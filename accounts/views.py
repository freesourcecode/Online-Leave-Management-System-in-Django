from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.urls import reverse
from .forms import UserRegisterForm
from accounts.forms import LoginForm
from employee.models import EmployeeDetails
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages


def register(request):
    context = {
        'form': UserRegisterForm(),
    }
    emp_obj = EmployeeDetails.objects.all()
    user_obj = User.objects.all()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=request.POST.get('email')).count() >= 1:
                context['form'] = UserRegisterForm(request.POST)
                context['error_msg'] = 'Email already registered !!!'
                return render(request, 'register.html', context)
            elif EmployeeDetails.objects.filter(email=request.POST.get('email')).count() >= 1:
                # Process to register
                user = form.save(commit=False)
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                username = request.POST.get('username')
                # Check Password with Confirm Password
                if not request.POST.get('password') == request.POST.get('confirm_password'):
                    context['error_msg'] = 'Password does not match the confirm password. !!!'
                    context['form'] = UserRegisterForm(request.POST)
                    return render(request, 'register.html', context)
                else:
                    password = request.POST.get('password')
                    user.set_password(password)
                    form.save()
                    context['success_msg'] = 'Registration Success. !!!'
                    context['form'] = UserRegisterForm(request.POST)
                    # Save user id in EmployeeDetails table
                    uid_obj = User.objects.get(email=request.POST.get('email'))
                    for e in emp_obj:
                        if e.email == request.POST.get('email'):
                            e.userid = uid_obj.id
                            e.save()
                    return render(request, 'register.html', context)
            else:
                context['form'] = UserRegisterForm(request.POST)
                context['error_msg'] = 'Email address does not exist. !!!'
                return render(request, 'register.html', context)
        elif User.objects.filter(username=request.POST.get('username')).count() >= 1:
            context['form'] = UserRegisterForm(request.POST)
            context['error_msg'] = 'Username already exists !!!'
            return render(request, 'register.html', context)
        else:
            context['error_msg'] = 'Invalid Email !!!'
            context['form'] = UserRegisterForm(request.POST)
            return render(request, 'register.html', context)
    return render(request, 'register.html', context)


# def register(request):
#     context = {
#         'register_form': UserRegisterForm(),
#     }
#     if request.method == 'POST':
#         print('Hello request')
#         register_form = UserRegisterForm(request.POST)
#         if register_form.is_valid():
#             print('Hello is valid')
#             register_form = UserRegisterForm(request.POST)
#             user = register_form.save(commit=False)
#             username = register_form.cleaned_data[register_form.username]  # request.POST.get('username')
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             user.set_password(password)
#             register_form.save()
#             context['message'] = 'Success !!!'
#             return render(request, 'login.html', context)
#         else:
#             context['message'] = 'Error !!!'
#             context['register_form'] = UserRegisterForm(request.POST)
#         return render(request, 'validate_user.html', context)
#     return render(request, 'validate_user.html', context)


# def validate_email(request):
#     context = {
#         'form': EmailValidateForm()
#     }
#     emp_obj = EmployeeDetails.objects.all()
#     if request.method == 'POST':
#         form = EmailValidateForm(request.POST)
#         if form.is_valid():
#             for emp in emp_obj:
#                 if emp.email == request.POST.get('email'):
#                     context['name'] = emp.name
#                     context['company'] = emp.company
#                     context['form'] = EmailValidateForm(request.POST)
#                     return render(request, 'register.html', context)
#         else:
#             context['error_msg'] = 'Invalid Email !!!'
#             context['form'] = EmailValidateForm(request.POST)
#             return render(request, 'register.html', context)
#         context['error_msg'] = 'Email address does not exist. !!!'
#         context['form'] = EmailValidateForm(request.POST)
#         return render(request, 'register.html', context)
#     return render(request, 'register.html', context)


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # return render(request, 'home.html', context)
            return HttpResponseRedirect(reverse(home_view))
        else:
            context['error_msg'] = 'Invalid username or password !!!'
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'login.html', {})


@login_required(login_url="/login/")
def home_view(request):
    context = {}
    context['user'] = request.user
    return render(request, 'home.html', context)


@login_required(login_url="/login/")
def change_password(request):
    context = {
        'form': PasswordChangeForm(request.user, request.POST)
    }
    form = PasswordChangeForm(request.user, request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = request.POST.get('password')
            user.set_password(password)
            form.save()
            # update_session_auth_hash(request, user)
            # messages.success(request, 'Password has been changed successfully. !!!')
            context['save_message'] = 'Password has been changed successfully. !!!'
            return render(request, 'change_password.html', context)
        else:
            # messages.error(request, 'Please correct the error below.')
            # context['error_msg'] = 'Invalid !!!'
            return render(request, 'change_password.html', {'form': form})
    return render(request, 'change_password.html', {'form': form})
