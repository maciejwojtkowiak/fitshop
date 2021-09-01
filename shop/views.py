from django.contrib.auth.models import User
from django.db.models import fields
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic.base import View
from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm, CommentCreationForm
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from shop.models import Comment, Item, Cart, OrderItem, Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .mixins import VisitCounter
import os 
import stripe
from django.http import JsonResponse
import json

stripe.api_key = os.environ.get('stripeAPI')

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
    def post(self, request, *args, **kwargs):
        return reverse('detail-page')


class ShopDetailView(VisitCounter, DetailView):
    model = Item 
    template_name = 'shop/detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(item=self.object)
        context['form'] = CommentCreationForm()
        return context

    def post(self, request, pk):
        if 'buy' in request.POST:
            item = get_object_or_404(Item, id=pk)
            orderItem, created = OrderItem.objects.get_or_create(order_item=item)
            cart, created = Cart.objects.get_or_create(order_user=request.user)
            cart.save()
            cart.order_items.add(orderItem)
            cart.total += item.price * orderItem.quantity
            cart.save()
            return HttpResponse('Items added to the database')
        if 'comment' in request.POST:
            form = CommentCreationForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.comment_user = request.user
                comment.item = Item.objects.get(id=pk)
                comment.save()
                return HttpResponse('post-created')
            else:
                return HttpResponse('post not created')
        
                

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

def profileView(request, pk):
    profile = Profile()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user,)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
    'profile': profile, 
    'u_form': u_form, 
    'p_form': p_form}
    return render(request, 'shop/profile.html', context)

class ProfileDeleteView(DeleteView):
    model = User
    template_name = 'shop/delete.html'
    fields = ['username', 'email']
    def get_success_url(self) -> str:
        return reverse('home-page')

def cart(request):
    cart = Cart.objects.filter(order_user=request.user)
    context = {'cart': cart}
    if request.method == 'POST':
        reverse('checkout-page')
    return render(request, 'shop/cart.html', context)

@csrf_exempt
def create_checkout_session(request, pk):

    request_data = json.loads(request.body)
    cart = Cart.objects.filter(order_user = request.user)

    stripe.api_key = os.environ.get('stripeAPI')
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email = request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': cart.order_items,
                    },
                    'unit_amount': cart.total,
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success-page')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('cancel-page')),
    )


def success(request):
    return render(request, 'shop/success.html')


def cancel(request):
     return render(request, 'shop/cancel.html')


    



