# accounts/views.py
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView
from .forms import UserRegistrationForm
from django.contrib.auth import login


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegistrationForm
    success_message = "Your account was created successfully"


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = ''  # Replace '/' with the URL you want to redirect to after login
