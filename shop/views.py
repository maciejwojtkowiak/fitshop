from django.shortcuts import render, redirect
from .forms import SignUpForm

def home(request):
    return render(request, 'shop/home.html')

def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid:
        pass 
    else: 
        form = SignUpForm()
    return render(request, "shop/signup.html", {'form': form})
