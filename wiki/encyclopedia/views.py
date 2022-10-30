from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import markdown2
from . import util
import random

titleList = []
for _ in util.list_entries():
    titleList.append((_,_))

class NewPageForm1(forms.Form):
    newTitle = forms.CharField(label="New Title")
class NewPageForm2(forms.Form):
    newContent = forms.CharField(label="New Content", widget=forms.Textarea(attrs={
        'size': '1', 'cols': "4", 'rows': "1"
        }))

class EditPageForm(forms.Form):
    newContent = forms.CharField(label="New Content", widget=forms.Textarea(attrs={'size': '4'}))
    
def index(request):
    if request.method == "POST":
        if request.POST["q"].upper() in map(str.upper,util.list_entries()):    
            return render(request, "encyclopedia/entryPage.html", {
            "title": request.POST["q"],
            "content": markdown2.markdown(util.get_entry(request.POST["q"]))
            })
        else:
            results = []
            for title in util.list_entries():
                if request.POST["q"].upper() in title.upper():
                    results.append(title)
            return render(request, "encyclopedia/searchresult.html",{
                "results":results
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entryPage(request,title):
    if title in util.list_entries():
        enablingEditing = True
        return render(request, "encyclopedia/entryPage.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title)),
            "enablingEditing": enablingEditing
        })
    enablingEditing = False
    return render(request, "encyclopedia/entryPage.html", {
            "title": title,
            "content": "<h1>Error</h1> The requested page was not found.",
            "enablingEditing": enablingEditing
        })

def searchResult(request):
    results=[]
    return render(request,"encyclopedia/searchresult.html",{
        "results":results
    })

def randomPage(request):
    title = random.choice(util.list_entries())
    return render(request, "encyclopedia/entryPage.html", {
        "title": "Random page: "+title,
        "content": markdown2.markdown(util.get_entry(title))
    })

def newPage(request):
    if request.method == "POST":
        form1 = NewPageForm1(request.POST)
        form2 = NewPageForm2(request.POST)
        if form1.is_valid() and form2.is_valid():
            title = form1.cleaned_data["newTitle"]
            content = form2.cleaned_data["newContent"]
            if title in util.list_entries():
                return render(request, "encyclopedia/entryPage.html", {
                "title": title,
                "content": f"<h1>This title, {title}, already exists!</h1>"
                })
            else:
                util.save_entry(title, content)
                return render(request, "encyclopedia/entryPage.html", {
                "title": title,
                "content": content
                })
    return render(request, "encyclopedia/newPage.html",{
        "form1": NewPageForm1,
        "form2": NewPageForm2
    })

def editPage(request):
    if request.method == "POST":
        form = EditPageForm(request.POST)      
        if form.is_valid():
            content = form.cleaned_data["newContent"]
            title = request.POST["title"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entryPage.html", {
            "title": title,
            "content": content
            })
            
    
    title = request.GET["newContent"]
    newContent = util.get_entry(title)

    return render(request, "encyclopedia/editPage.html",{
        "form": EditPageForm({"newContent": newContent}),
        "title": title
    })
