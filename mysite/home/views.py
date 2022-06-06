from django.shortcuts import render
from .models import Document
from . import models


# Create your views here.

TEMPLATE_DIRS = (
    'os.path.join(BASW_DIR , "templates"),'
)


def index(request):
    return render(request , "index.html" )

def login(request):
    return render(request , "login.html")

def create(request):
    if request.method == "POST":
        upload_files = request.FILES["FILES"]
        
        docs=models.Document(
            FILES=upload_files
        )
        
        docs.save()
    return render(request , "create.html")


def revise(request):
    if request.method == "POST":
        upload_files = request.FILES["FILES"]
        
        docs=models.Document(
            FILES=upload_files
        )
        
        docs.save() 
    return render(request , "revise.html")

def delete(request):
    return render(request , "delete.html")

def finish(request):
    documents = models.Document.objects.all()
    
    return render(request ,
                  "finish.html" ,
                  {"documents" : documents})

def schedule(request):
    return render(request , "schedule.html")

def test(request):
    return render(request , "test.html")

def depsform(request):
    return render(request, "depsform.html")