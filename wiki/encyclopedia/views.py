from django.shortcuts import render
from django import forms
from django.http import * 
from render_block import render_block_to_string
import markdownify
from . import util
from random import randint
import markdown

class Searchbar(forms.Form):
    srch = forms.CharField(label="Search")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":Searchbar()
    })

def items(request, name):
    entries = util.list_entries()
    name = name[:name.find('.')]
    for entry in entries:
        if name == entry:
            html = f"encyclopedia/{name}.html"
            return render(request, html,{
                "form":Searchbar()
            })
    return HttpResponse("Not Found!")

def query(request, query):
    entries = util.list_entries()
    req = query.upper()
    z=''
    results =[]
    if request.method == "POST":
        form = Searchbar(request.POST)
        if  form.is_valid():
            a = form.cleaned_data["srch"]
            z=a.upper()
    for entry in entries:
        if req == entry.upper():
            html = f"encyclopedia/{req}.html"
            return render(request, html,{
                "form":Searchbar()
            })
        elif z == entry.upper():
            html = f"encyclopedia/{z}.html"
            return render(request, html,{
                "form":Searchbar()
            })
        elif z in entry.upper():
            for c in entry.upper():
                if c in z:
                    results.append(entry)
                    break
                    
    if len(results) == 0:
        return HttpResponse("NOT FOUND!")
    return render(request, "encyclopedia/index.html", {
        "entries": results,
        "form":Searchbar()
    })

def random(request):
    entries = util.list_entries()
    n = len(entries)-1
    r = randint(0,n)
    return render(request, f"encyclopedia/{entries[r]}.html", {
        "form":Searchbar()
    })

def create(request):
    return render(request, 'encyclopedia/createnew.html',{
                "form":Searchbar()
            })
def new(request):
    data = request.POST['c']
    title = request.POST['title']
    #The 'safe' tag in html to convert str with html tags to be read as html
    entries = util.list_entries()
    data_out = markdown.markdown(data)
    for entry in entries:
        if title == entry:
            return HttpResponse("This title already exists!\n Please go back and change title or go to Edit page to change existing page!")
    util.save_entry(title,data)
    with open('encyclopedia/templates/encyclopedia/tmplt.html', 'rb') as f:
        text = f.read().decode("utf-8")
    with open(f'encyclopedia/templates/encyclopedia/{title}.html', 'w') as f:
        f.write(text)
        f.write(data_out)
        f.write("{% endblock %}")
    return render(request, 'encyclopedia/newpage.html', {'data':data_out,'title':title,"form":Searchbar()})

def edit(request):
    url = request.META.get('HTTP_REFERER')
    title = url[url.rfind('/')+1:]
    html=render_block_to_string(f'encyclopedia/{title}.html', 'body')
    h = markdownify.markdownify(html, heading_style="ATX")
    return render(request, 'encyclopedia/editpage.html',{
        'title':title,
        'body':h
    })

def sub_edit(request):
    data = request.POST['c']
    title = request.POST['title']
    data_out = markdown.markdown(data)
    util.save_entry(title,data)
    with open('encyclopedia/templates/encyclopedia/tmplt.html', 'rb') as f:
        text = f.read().decode("utf-8")
    with open(f'encyclopedia/templates/encyclopedia/{title}.html', 'w') as f:
        f.write(text)
        f.write(data_out)
        f.write("{% endblock %}")
    return render(request, 'encyclopedia/newpage.html', {'data':data_out,'title':title,"form":Searchbar()})