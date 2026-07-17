from django.shortcuts import redirect, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User
from django.contrib.auth import logout
from .forms import (
    ClientRegistrationForm,
    CounsellorRegistrationForm,
    LoginForm
)


# Create your views here.
def register(request):
    return render(request, "accounts/register.html")


def register(request):
    """Registration choice page."""
    return render(request, "accounts/register.html")


def client_register(request):
    if request.method == "POST":
        form = ClientRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Client account created successfully.")
            return redirect("login")     
    else:
        form = ClientRegistrationForm()

    return render(request, "accounts/client_register.html", {
        "form": form
    })


def counsellor_register(request):
    return render(request, "accounts/counsellor_register.html")


def login_view(request):
    form = LoginForm(request=request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Welcome back!")
            return redirect("home")      # change if needed

    return render(request, "accounts/login.html", {
        "form": form
    })

def logout_view(request):
    logout(request)
    messages.success(
        request,
        "You have been logged out successfully."
    )
    return redirect("login")