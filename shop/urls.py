from django.urls import path
from . import views
from .views import ShopListView, ShopDetailView,ProfileDeleteView
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
    path('profile', views.profileView, name='profile-page'),
    path('delete/<int:pk>/', ProfileDeleteView.as_view(), name ='delete-page'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)