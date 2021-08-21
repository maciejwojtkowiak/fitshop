from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from django.views.generic.list import ListView
from shop.models import Item

def home(request):
    items = Item.objects.all()
    args = {'items': items}
    return render(request, 'shop/home.html', args)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f" {username} your account was created!")
            return redirect('home-page') 
    else: 
        form = SignUpForm()
    return render(request, "shop/signup.html", {'form': form})


