from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import login_view, logout_view, home_view
from .views import *
from . import views


urlpatterns = [
    path('login/', login_view, name='login'),
    path('', login_view, name='login'),
    path('accounts/login/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('register/', register, name='register'),
    path('accounts/change_password/', views.change_password, name='change_password'),
]
