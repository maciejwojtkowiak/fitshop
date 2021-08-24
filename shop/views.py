from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from shop.models import Item
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.http import Http404
from django.db.models import Avg, Max, Min
from django.db.models import Q

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
        else:
            form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

def logoutView(request):
    logout(request)
    return redirect('home-page')

class ShopListView(ListView):
    model = Item
    template_name =  'shop/home.html'
    context_object_name = 'items'


class ShopDetailView(DetailView):
    model = Item 
    template_name = 'shop/detail.html'
    context_object_name = 'item'

def searchView(request):
    if request.method == "GET":
        context = request.GET.get('search')
        items = Item.objects.all().filter(title__icontains=context)

    return render(request, 'shop/search.html', {'items': items})

def sortView(request): 
    if request.method == "GET":
        sorting_method = request.GET.get('select')
        if sorting_method == 'v1':
            items = Item.objects.order_by('price')
        if sorting_method == 'v2':
            items = Item.objects.order_by('-price')
        
    return render(request, 'shop/sort.html', {'items': items})

