from django.contrib.auth.models import User
from django.core import paginator
from django.db.models.expressions import F
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm, CommentCreationForm, LoginForm
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from shop.models import Comment, Item, Cart, OrderItem, Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from .mixins import VisitCounter
from django.views.generic import TemplateView
import os 
import stripe
from django.db.models import Sum
from django.core.paginator import Paginator


stripe.api_key = os.environ.get('stripeAPI')
search_history = []

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
        form = LoginForm(request, data=request.POST)
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
                form = LoginForm()
        else:
            form = LoginForm()
    else:
        form = LoginForm()
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
        context['comments'] = Comment.objects.filter(comment_item=self.object)
        context['form'] = CommentCreationForm()
        return context

    def post(self, request, pk):
        if 'buy' in request.POST:
            item = get_object_or_404(Item, id=pk)
            cart = Cart.objects.get(order_user = request.user)
            orderItem, created = OrderItem.objects.get_or_create(item=item, cart=cart)
            if not created: 
                orderItem.quantity = F('quantity') + 1
                orderItem.save(force_update=True, update_fields=['quantity'])
            cart.order_items.add(orderItem.item)
            cart.save()
            return redirect('cart-page', pk=self.request.user)
        if 'comment' in request.POST:
            form = CommentCreationForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.comment_user = request.user
                comment.comment_item = Item.objects.get(id=pk)
                comment.save()
                return HttpResponse('detail-page')
            else:
                return HttpResponse('detail-page')
        
def searchView(request):
    if request.method == "POST":
        context = request.POST.get('search')
        if not context:
            context = search_history[-1]
        search_history.append(context)
        items = Item.objects.all().filter(title__icontains=search_history[-1])
        try:
            sorting_method = request.POST.get('select')
            if sorting_method == 'v1':
                items = items.order_by('price')
                return render(request, 'shop/search.html', {'items': items})
            if sorting_method == 'v2':
                items = items.order_by('-price')
                return render(request, 'shop/search.html', {'items': items})
            else:
                return render(request, 'shop/search.html', {'items': items})
        except UnboundLocalError:
            return redirect('home-page')
        


def sortView(request): 
    if request.method == "POST":
        try:
            sorting_method = request.POST.get('select')
            if sorting_method == 'v1':
                items = Item.objects.order_by('price')
            if sorting_method == 'v2':
                items = Item.objects.order_by('-price')
            return render(request, 'shop/sort.html', {'items': items})
        except UnboundLocalError:
            return redirect('home-page')

def profileView(request, pk):
    profile = Profile()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
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
class CartView(TemplateView):
    template_name = "shop/cart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart.objects.annotate(
        price=Sum(F('orderitem__item__price') * F('orderitem__quantity'))
        ).get(order_user= self.request.user)
        cart = context['cart']
        cart.total = cart.price
        cart.save()  
        context['order_items'] = OrderItem.objects.filter(cart=cart)
        return context
    def post(self, request, pk):
        if 'minus' in request.POST:
            cart = Cart.objects.get(order_user=self.request.user)
            item = OrderItem.objects.filter(id=pk, cart=cart, quantity__lte=1)
            if not item.delete()[0]:
                OrderItem.objects.filter(
                id=pk, cart=cart).update(quantity=F('quantity')-1)
            return redirect('cart-page', pk=self.request.user)
        if 'plus' in request.POST:
            cart = Cart.objects.get(order_user=self.request.user)
            OrderItem.objects.filter(id=pk, cart=cart).update(
            quantity=F('quantity')+1)
            return redirect('cart-page', pk=self.request.user)
        if 'delete' in request.POST:
            cart = Cart.objects.get(order_user=self.request.user)
            item = OrderItem.objects.filter(id=pk, cart=cart).delete()
            return redirect('cart-page', pk=self.request.user)

   
@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        try:
            line = []
            cart = Cart.objects.get(order_user=request.user)
            for item in cart.order_items.all():
              product={'price_data':{'currency': 'eur', 'product_data':{'name':item.title},'unit_amount': item.price}, 'quantity': OrderItem.objects.get(cart=cart, item=item).quantity }
              line.append(product)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card', 'p24'], 
                    line_items= line,
                mode='payment',
                success_url = request.build_absolute_uri(reverse('success-page'))+ '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url = request.build_absolute_uri(reverse('cancel-page')),
            )
        except Exception as e:
            return HttpResponse(e)
        return redirect(checkout_session.url, code=303)
            
 

def success(request):
    return render(request, 'shop/success.html')


def cancel(request):
     return render(request, 'shop/cancel.html')


    
