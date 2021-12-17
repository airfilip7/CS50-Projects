from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# from django import forms
# from .models import *
from .forms import *
from .util import *
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
    
@register.filter(name='lookup')
def get_item(dictionary, key):
    if type(dictionary) == dict:
        return dictionary.get(key)
    return None

def index(request):
    items = Item.objects.filter(is_closed=False)
    list = []
    dict = {}
    for item in items:
        highest_bid = filter_or_none(Bid, item__pk=item.pk)
        highest_bid = get_max_value(highest_bid, "bid")
        list.append(highest_bid)
        
    var = 0
    for bid in list:
        item = Item.objects.all()[var]
        dict[item.pk] = list[var]
        var += 1
    return render(request, "auctions/index.html", {
        "items": items,
        "current": dict,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register1(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def categories(request, filter):
    if not filter :
        return render(request, "auctions/categories.html", {
            "list": CATEGORIES
        })
    else:
        for var in CATEGORIES:
            if filter in var[1]:
                return render(request, "auctions/index.html", {
                    "items": Item.objects.filter(category=filter),
                    "message": "No items in " + var[1]
                })
        message = "Category doesn't exist" 
        return render(request, "auctions/errors.html", {
                "message": message
            }) 
        
@login_required
def watchlist(request):
    user = request.user
    list = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "user": user,
        'list': list
    })

@login_required
def view(request, title):
    item = get_or_none(Item, name=title)
    if not item:
        error = "No listing found with the name " + title
        return render(request, "auctions/errors.html", {
            "message": error
        })
    usr = request.user
    is_publisher = item.publisher.pk
    usr_watchlist = usr.watchlist.filter(pk=item.pk)
    highest_bid_obj = filter_or_none(Bid, item__pk=item.pk)
    highest_bid = get_max_value(highest_bid_obj, "bid")
    message = None
    comments = Comment.objects.filter(item__pk=item.pk).order_by('-date_posted')
    
    if not highest_bid:
        form = BidForm(initial={"bid": item.starting})
    else:
        form = BidForm(initial={"bid": highest_bid})
    comm_form = CommentForm()
    
    if request.method == "POST":
        if request.POST.get('add'):
            usr.watchlist.add(item) 
        if 'remove' in request.POST:
            usr.watchlist.remove(item)
        if 'close' in request.POST:
            item.is_closed = True
            item.save()
            return HttpResponseRedirect(reverse("view", args={item.name}))
        if 'comment' in request.POST:
            comm_form = CommentForm(request.POST)
            data = comm_form.save(commit=False)
            data.user = usr
            data.item = item
            data.save()
            return HttpResponseRedirect(reverse("view", args={item.name}))
        if 'place_bid' in request.POST:
            form = BidForm(request.POST)
            if form.is_valid():
                BID = form.cleaned_data["bid"]
                if not highest_bid:
                    if BID <= item.starting:
                        message = "Bid must be higher than the starting price."
                        return render(request, "auctions/item.html", {
                            "title": title,
                            "item": item,
                            "publisher": item.publisher,
                            "user_watchlist": usr_watchlist,
                            "is_closed": item.is_closed,
                            "form": form,
                            "comm_form": comm_form,
                            "comments": comments,
                            'current': highest_bid,
                            'error': message
                        })
                else:
                    if BID <= highest_bid:
                        message = "Bid must be higher than the current bid."
                        return render(request, "auctions/item.html", {
                            "title": title,
                            "item": item,
                            "publisher": item.publisher,
                            "user_watchlist": usr_watchlist,
                            "is_closed": item.is_closed,
                            "form": form,
                            "comm_form": comm_form,
                            "comments": comments,
                            'current': highest_bid,
                            'error': message
                        })
                data = form.save(commit=False)
                data.bidder = usr
                data.item = item
                data.save()
                return render(request, "auctions/item.html", {
                    "title": title,
                    "item": item,
                    "publisher": item.publisher,
                    "user_watchlist": usr_watchlist,
                    "is_closed": item.is_closed,
                    "form": form,
                    "comm_form": comm_form,
                    "comments": comments,
                    'current': get_max_value(filter_or_none(Bid, item__pk=item.pk), "bid"),
                    'message': "Succesfully placed bid"
                })
        
    if item.is_closed:
        return render(request, "auctions/closed_item.html", {
            "title": title,
            "item": item,
            "winner": filter_or_none(Bid, item__pk=item.pk).order_by('-bid').first().bidder.username,
            "publisher": item.publisher,
            "comments": comments,
            'current': highest_bid,
        })
    else:
        return render(request, "auctions/item.html", {
            "title": title,
            "item": item,
            "publisher": item.publisher,
            "user_watchlist": usr_watchlist,
            "is_closed": item.is_closed,
            "form": form,
            "comm_form": comm_form,
            "comments": comments,
            'current': highest_bid,
            'message': message
        })

@login_required
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.publisher = request.user
            data.pk = 4
            data.save()
            return HttpResponseRedirect(reverse("index")) 
        else: 
            return render(request, "auctions/errors.html", {
                "form": form
            })       
    else:
        form = CreateForm()
        
    return render(request, "auctions/create.html", {
        "form": form
    })
        
