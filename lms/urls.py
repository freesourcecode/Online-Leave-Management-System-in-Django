"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from accounts.forms import LoginForm
from accounts.views import *
import accounts.views
from employee.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('accounts.urls')),
    # path('register/', accounts.views.register, name='register'),
    # path('login/', auth_views.LoginView, {'template_name': 'login.html', 'authentication_form': 'LoginForm'}),
    # path('logout/', auth_views.LogoutView, {'next_page': '/login'}),
    path('employee/', include('employee.urls')),
    path('leave/', include('applyleave.urls')),
    # path('myleave/', include('applyleave.urls')),
    #path('teamleave/', include('applyleave.urls')),
]

