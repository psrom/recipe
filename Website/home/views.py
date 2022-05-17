from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    print(request.user)
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        return render(request, 'signup.html')