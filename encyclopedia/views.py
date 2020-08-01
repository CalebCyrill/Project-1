from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django import forms
from django.urls import reverse, reverse_lazy
import random
import markdown2

from . import util


class NewEntry(forms.Form):
    """ 
    To access the forms in Django
    """
    title = forms.CharField(max_length=250)
    content = forms.CharField(widget=forms.Textarea)


def index(request):
    """
    This will access the landing page
    """
    pName = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": pName
    })


def page(request, pagename):
    """
    This will setup the individual pages for each entry
    """
    pName=util.get_entry(pagename.capitalize())
    if pName == None:
        raise Http404
    else:
        content = markdown2.markdown(pName)
        return render(request, "encyclopedia/page_framework.html", {
            "name": pagename.capitalize(), "content": content
            })


def search(request):
    """
    This will allow the search bar to return results
    """
    pName = util.list_entries()
    query = request.GET.get('q')
    if query in pName:
        return redirect("page", pagename=query)
    else:
        results = []
        for page in pName:
            page1 = page.lower()
            if query.lower() in page1:
                results.append(page)
        return render(request, "encyclopedia/search.html", {
            "result": results, "query": query
        })


def create(request):
    """
    This will take the user to the template to create a new entry
    """
    context = {}
    context['form'] = NewEntry()
    return render(request, "encyclopedia/create.html", context)


def exist(request):
    """
    This will redirect the user to a page that tells the user that the page they are trying to create already exists
    """
    return render(request, "encyclopedia/exists.html")


def newPage(request):
    """
    This will take the user to the newly created entry 
    """
    pName = util.list_entries()
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            title = form.cleaned_data["title"]
            if title in pName:
                return redirect('exists')
            else:
                util.save_entry(title, content)
                title = request.POST["title"]
                return redirect('page', pagename=title)


def editPage(request, name):
    """
    This will take the user to a form where they can edit the page they are on
    """
    content = util.get_entry(name)
    context = {}
    context['form'] = NewEntry(initial={'title': name, 'content': content})
    return render(request, "encyclopedia/editpage.html", context)


def edit(request):
    """
    This will take the user to newly editted page 
    """
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('page', pagename=title)


def randomPage(request):
    """
    This will allow the user to go to a random page in the list of encyclopedia entries
    """
    page = random.choice(util.list_entries())
    return redirect('page', pagename=page)
    