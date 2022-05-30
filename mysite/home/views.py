from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

TEMPLATE_DIRS = (
    'os.path.join(BASW_DIR , "templates"),'
)


def index(request):
    return render(request , "index.html" )

def login(request):
    return render(request , "login.html")

def create(request):
    return render(request , "create.html")

def revise(request):
    return render(request , "revise.html")

def delete(request):
    return render(request , "delete.html")

def finish(request):
    return render(request , "finish.html")

def schedule(request):
    return render(request , "schedule.html")

def test(request):
    return render(request , "test.html")

def depsform(request):
    return render(request, "depsform.html")