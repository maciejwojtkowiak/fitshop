from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from django.views.generic.list import ListView
from shop.models import Item
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

def home(request):
    items = Item.objects.all()
    args = {'items': items}
    return render(request, 'shop/home.html', args)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f" {username} your account was created!")
            return redirect('login-page') 
    else: 
        form = SignUpForm()
    return render(request, "shop/signup.html", {'form': form})

def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user = form.cleaned_data.get('username')
                messages.success(request, f"You successfully logged in {user}")
                return redirect('home-page')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home-page')

def homeView(ListView):
    model = Item


