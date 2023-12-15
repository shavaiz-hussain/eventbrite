# accounts/views.py
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView

from .forms import UserRegistrationForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")
    form_class = UserRegistrationForm
    success_message = "Your account was created successfully"


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    success_url = ""  # Replace '/' with the URL you want to redirect to after login
