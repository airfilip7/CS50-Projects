from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.core.serializers import serialize
from .models import *
from django import template
from django.utils.safestring import mark_safe
from django.template.defaulttags import register
from django.core.paginator import Paginator


def get_fllw_or_none(request, *args, **kwargs):
    try:
        return request.user.following.get(*args, **kwargs)
    except User.DoesNotExist:
        return None

@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()
        
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, "network/index.html", {
            "page_obj": page_obj,
        })
    else:
        return HttpResponseRedirect(reverse('login'))

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def add(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    content = data.get("content", "")
    if content == "":
        return JsonResponse({'error': 'Cannot add post without content.'}, status=400)
    
    post = Post(
        User = request.user, 
        content = content,
    )
    post.save()
    return JsonResponse({'message': 'Post added to the feed succesfully.', }, status=200)
    

@csrf_exempt
@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": f"User with username {username} does not exist"}, status=400)

    if request.method == "PUT":
        data = json.loads(request.body)
        follow = data.get("follow", "")
        if not follow:
            request.user.following.remove(user)
            user.followers.remove(request.user)
        else:
            request.user.following.add(user)
            user.followers.add(request.user)
        return JsonResponse(user.serialize(), status=200)
    
    posts = Post.objects.filter(User=user)
    posts = posts.order_by("-timestamp").all()
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/profile.html", {
        "user1": user,
        "page_obj": page_obj,
        "follows": get_fllw_or_none(request, pk=user.pk)
    })
    

@csrf_exempt
@login_required
def edit(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    data = json.loads(request.body)
    content = data.get("content", "")
    pk = data.get("pk", "")
    if not content:
        return JsonResponse({"error": "Post must contain some text."}, status=400)
    
    post = Post.objects.get(pk=pk)
    post.content = content
    post.save()
    
    return JsonResponse({'message': 'Post updated succesfully.'}, status=200)


@csrf_exempt
@login_required
def like(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    data = json.loads(request.body)
    pk = data.get("pk", "")
    liked = data.get("liked", "")
    
    post = Post.objects.get(pk=pk)
    if liked:
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)
    post.save()
    
    return HttpResponse(status=204)


@login_required
def following(request):
    user = User.objects.get(pk=request.user.pk)
    following = user.following.all()
    pks = []
    for usr in following:
        pks.append(usr.pk)
    posts = Post.objects.filter(User__pk__in=pks).order_by('-timestamp').all()
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
            
    return render(request, "network/following.html", {
        "page_obj": page_obj,
    })
