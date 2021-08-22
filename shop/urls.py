from django.urls import path
from . import views
from .views import ShopListView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', ShopListView.as_view(), name='home-page'),
    path('signup', views.signup, name='signup-page'),
    path('login', views.loginView, name='login-page'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)