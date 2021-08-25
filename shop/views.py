from django.contrib.auth.models import User
from django.db.models import fields
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import (
SignUpForm, 
ProfileUpdateForm, 
UserUpdateForm, 
CommentCreationForm)
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from shop.models import Item, Profile, Comment
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout


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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentCreationForm()
        return context

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

def profileView(request):
    profile = Profile
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user,)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    args = {
    'profile': profile, 
    'u_form': u_form, 
    'p_form': p_form}
    return render(request, 'shop/profile.html', args)

class ProfileDeleteView(DeleteView):
    model = User
    template_name = 'shop/delete.html'
    fields = ['username', 'email']
    def get_success_url(self) -> str:
        return reverse('home-page')



    



