from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from . import util
from django.core.exceptions import ValidationError
import markdown2
from django import forms
import re
from random import randrange
from django.urls import reverse



class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter title...'}))
    md = forms.CharField(label="Markdown", widget=forms.Textarea(attrs={'placeholder': "Enter content...", 'rows': 1, "cols": 10, "class": "align-text-top" })) #initial= continutul md
    
# class EntryForm(forms.Form):
#     entry = forms.CharField(max_length=100)  ### used in the commented search function
    
class EditPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, disabled=True, required=False)
    md = forms.CharField(label="Markdown", widget=forms.Textarea(attrs={'placeholder': "Enter content...", 'rows': 1, "cols": 10, "class": "align-text-top"})) #initial= continutul md

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["md"]
            if not util.get_entry(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('view', args={title}))
            else:
                 content = "Entry already exits"
                 return render(request, "encyclopedia/error.html", {
                     "content": content
                 })
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })

def rand_page(request):
    list = util.list_entries()
    rand = randrange(len(list))
    file = list[rand]
    return view(request, file)

def view(request, title):
    file = util.get_entry(title)
    if not file:
        return render(request, "results/no_result.html")
    else:
        html = markdown2.markdown(file)
        return render(request, "encyclopedia/entry.html", {
            "title": title,"content": html
        })

# def search(request):
#     if request.method == "POST":
#         form = EntryForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data["entry"]
#             if util.get_entry(data):
#                 return HttpResponseRedirect('/wiki/' + data)
#             else:
#                 list = []
#                 entries = util.list_entries()
#                 for entry in entries:                                 ### I commented this function because I couldn't figure out a way to render the form input field
#                     if re.search(data, entry, re.IGNORECASE):             and decided to use the <input> tag. I also have trouble understanding how to style django generated items
#                         list.append(entry)                                with widgets. I have seen some classes that have a Model in them, but I don't know anything about them because
#                 if not list:                                              I have only watched the first 4 lessons. If you have the necessary time, I will be grateful to know if there is a
#                     return render(request, "results/no_result.html")      better way to solve this problem. 
#                 else:
#                     return render(request, "results/succ_result.html", {
#                         "list": list
#                     })
#     else:
#         form = EntryForm()
    
#     return render(request, "encyclopedia/index.html", {
#         "form": form
#     })
    
def search(request):
    if request.method == "POST":
        data = request.POST["entry"]
        if util.get_entry(data):
            return HttpResponseRedirect('/wiki/' + data)
        else:
            list = []
            entries = util.list_entries()
            for entry in entries:
                if re.search(data, entry, re.IGNORECASE):
                    list.append(entry)
            if not list:
                return render(request, "results/no_result.html")
            else:
                return render(request, "results/succ_result.html", {
                    "list": list
                })
 
    return render(request, "encyclopedia/index.html")
    
def edit(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            # title = form.cleaned_data["title"]
            content = form.cleaned_data["md"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('view', args={title}))
    else:
        file = util.get_entry(title)
        form = EditPageForm(initial={"title": title, "md": file})
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form
    })

    
            
        