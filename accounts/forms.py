from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=30, required=True,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'name': 'first_name',
                                     'type': 'text',
                                     'id': 'first_name',
                                     'placeholder': 'First Name'
                                 }))
    last_name = forms.CharField(label='Last Name', max_length=150, required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'name': 'last_name',
                                    'type': 'text',
                                    'id': 'last_name',
                                    'placeholder': 'Last Name'
                                }))
    email = forms.EmailField(label="Email", max_length=254, required=True,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'name': 'email',
                                 'type': 'email',
                                 'id': 'email',
                                 'placeholder': 'Enter work email'
                             }))
    username = forms.CharField(label='Username', max_length=150, required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'name': 'username',
                                   'type': 'text',
                                   'id': 'username',
                                   'placeholder': 'Username'
                               }))
    password = forms.CharField(label="Password", max_length=128, required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'name': 'password',
                                   'type': 'password',
                                   'id': 'password',
                                   'placeholder': 'Password'
                               }))
    confirm_password = forms.CharField(label="Confirm Password", max_length=128, required=True,
                                       widget=forms.PasswordInput(attrs={
                                           'class': 'form-control',
                                           'name': 'confirm_password',
                                           'type': 'password',
                                           'id': 'confirm_password',
                                           'placeholder': 'Confirm Password'
                                       }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


# class EmailValidateForm(forms.Form):
#     email = forms.EmailField(required=True, label="Email",
#                              widget=forms.EmailInput(attrs={
#                                  'class': 'form-control',
#                                  'name': 'email',
#                                  'type': 'email',
#                                  'id': 'email',
#                                  'placeholder': 'Enter work email'
#                              }))
