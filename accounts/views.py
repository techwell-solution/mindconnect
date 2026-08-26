from django.shortcuts import redirect, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User, ClientProfile
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import (
    ClientRegistrationForm,
    CounsellorRegistrationForm,
    LoginForm, 
    UserUpdateForm, 
    ClientProfileForm
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
    if request.method == "POST":
        form = CounsellorRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("login")   # Use your actual login URL name
        else:
            print(form.errors)   # Check your terminal

    else:
        form = CounsellorRegistrationForm()

    return render(
        request,
        "accounts/counsellor_register.html",
        {"form": form},)


def login_view(request):
    form = LoginForm(request=request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, "Welcome back!")

            if user.role == User.CLIENT:
                return redirect("client_dashboard")

            elif user.role == User.COUNSELLOR:
                return redirect("counselor_dashboard")

            elif user.role == User.ADMIN:
                return redirect("admin_dashboard")

            return redirect("home")

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
@login_required
def gen_dashboard(request):
    return render(request, 'accounts/gen_dashboard.html')
    
@login_required
def update_profile(request):

    profile, created = ClientProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ClientProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("update_profile")

    else:

        user_form = UserUpdateForm(instance=request.user)

        profile_form = ClientProfileForm(instance=profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "profile": profile,
    }

    return render(
        request,
        "accounts/update_profile.html",
        context,
    )

@login_required
def settings_view(request):
    return render(request, "accounts/settings.html")