from django.urls import path
from . import views
from .views import (
ShopListView, 
ShopDetailView,
ProfileDeleteView,)
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', ShopListView.as_view(), name='home-page'),
    path('signup', views.signup, name='signup-page'),
    path('login', views.loginView, name='login-page'),
    path('logout', views.logoutView, name='logout-page'),
    path('detail/<int:pk>/', ShopDetailView.as_view(), name='detail-page'),
    path('search', views.searchView, name='search-page'),
    path('sort', views.sortView, name='sort-page'),
    path('profile/<str:pk>', views.profileView, name='profile-page'),
    path('delete/<int:pk>/', ProfileDeleteView.as_view(), name ='delete-page'),
    path('cart', views.cart, name='cart-page'),
    path('create_checkout_session/<int:pk>', views.create_checkout_session, name='checkout-page'), 
    path('success', views.success, name='success-page'),
    path('cancel', views.cancel, name='cancel-page')
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)