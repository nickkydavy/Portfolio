from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from markdown2 import Markdown

from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label="")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def wiki(request, title):
    for entry in util.list_entries():
        markdowner = Markdown()
        if(title == entry):
            content = markdowner.convert(util.get_entry(title))
            return render(request, "encyclopedia/content.html", {
                "form": SearchForm(),
                "name": title,
                "content": content
                })
    return render(request, "encyclopedia/content.html", {
                "form": SearchForm(),
                "name": title,
                "content": None
                })        

def search_entry(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['q']
            for entry in util.list_entries():
                if search == entry:
                    return HttpResponseRedirect(f"../wiki/{search}")
            return render(request, "encyclopedia/search_entry.html", {
                "search_result": search,
                "form": form
            })

    return render(request, "encyclopedia/index.html", {
        "form": SearchForm()
    })