from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
import markdown2
import random 
import time 
class SearchForm (forms.Form):
    search = forms.CharField(label = "Search Encyclopedia" 
    # widget = forms.TextInput(attrs=
    #{'placeholder': 'Search Encyclopedia'})
    )

class NewPage (forms.Form):
    title = forms.CharField ( label = "Title of Page" , 
    widget = forms.TextInput (attrs = {'placeholder': 'Enter Title Here'}) )
    text_content = forms.CharField (# abel = "text_content"
    widget = forms.Textarea (attrs = {'placeholder':'Enter Entry Content Here'})
     )

class EditContent(forms.Form):
    text_content = forms.CharField (
        widget = forms.Textarea
    )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })

def entry(request, name = "" ):
    content = util.get_entry(name) 
    if content == None :
        content = "404 Error. Requested Page Was Not Found."
        name = "Error"
    return render ( request, "encyclopedia/entry.html", { 
        "content": markdown2.markdown(content),
        "title": name,
        "search_form": SearchForm()
    }
    )

def search(request):
    form = SearchForm(request.GET)
    search = None
    lowerlist_entries = [ string.lower() for string in  util.list_entries()]
    if form.is_valid():
        search = form.cleaned_data["search"]
        if search.lower() in lowerlist_entries:
            return  HttpResponseRedirect(reverse ('entry', kwargs = { 'name' :search})) #   entry (request, search )
    substring_list = []
    if search != None:
        for item in util.list_entries():
            if search.lower() in item.lower(): 
                substring_list.append (item)
    return render ( request, "encyclopedia/search.html",  {
        "search_results" : substring_list ,
        "search_form" : SearchForm()
    })
    
def create_page (request):
    if request.method == "POST" :
        form = NewPage(request.POST)
        if form.is_valid ():
            title = form.cleaned_data ["title"]
            if title.lower() in [ string.lower() for string in   util.list_entries()] :
                return HttpResponseRedirect(reverse("create_page_error")  )
            content = form.cleaned_data ["text_content"]
            util.save_entry(title,content)
            return  HttpResponseRedirect(reverse("entry" , kwargs= {'name' : title}))     # entry (request, title ) 
        else :
            return render ( request, 'encyclopedia/create_page.html' , {
                "new_page" : form,  "search_form" : SearchForm()
            })

    return render (request, 'encyclopedia/create_page.html' ,  {
        "new_page" : NewPage(),
        "search_form" :SearchForm()
    })
def create_page_error (request):
    return render (request, 'encyclopedia/create_page_error.html', {
                    "search_form" :SearchForm()
                })
def random_page ( request):
    random.seed(time.time())
    list_entries = util.list_entries()
    index = random.randrange( 0, len( list_entries ))
    return HttpResponseRedirect( reverse ( 'entry'  ,  kwargs = { 'name': list_entries[index] }  )  )

def edit (request, name = ""):
    if request.method == "POST":
        form = EditContent(request.POST)
        if form.is_valid ():
            content = form.cleaned_data["text_content"]
            util.save_entry(name, content )
            return HttpResponseRedirect (reverse ('entry', kwargs = {'name' : name}   ))
        else :
            return render (request, "encyclopedia/edit_entry.html", {
                "edit_content" : form,
                "search_form": SearchForm(),
                "title" : name 
            })
    return render ( request, 'encyclopedia/edit_entry.html', {
        "search_form": SearchForm(),
        "edit_content" : EditContent( initial = { 'text_content' : util.get_entry(name)}  ),
        "title" : name 
    })
