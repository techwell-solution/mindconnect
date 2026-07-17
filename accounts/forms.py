from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ClientProfile, CounsellorProfile
from django.contrib.auth.forms import AuthenticationForm


class ClientRegistrationForm(UserCreationForm):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "phone_number": "Phone Number",
            "password1": "Password",
            "password2": "Confirm Password",
        }

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
                "placeholder": placeholders.get(field, ""),
            })

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.role = User.CLIENT

        if commit:
            user.save()
            ClientProfile.objects.create(user=user)

        return user
    
class CounsellorRegistrationForm(UserCreationForm):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)

    professional_title = forms.CharField(max_length=100)
    specialization = forms.CharField(max_length=100)
    years_of_experience = forms.IntegerField()
    license_number = forms.CharField(max_length=100)

    qualifications = forms.CharField(
        widget=forms.Textarea
    )

    bio = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

    profile_photo = forms.ImageField(required=False)
    license_document = forms.FileField(required=False)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "phone_number": "Phone Number",
            "professional_title": "Professional Title",
            "specialization": "Specialization",
            "years_of_experience": "Years of Experience",
            "license_number": "License Number",
            "qualifications": "Qualifications",
            "bio": "Tell us about yourself",
            "password1": "Password",
            "password2": "Confirm Password",
        }

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
                "placeholder": placeholders.get(field, ""),
            })

        self.fields["bio"].widget.attrs["rows"] = 4
        self.fields["qualifications"].widget.attrs["rows"] = 4

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.role = User.COUNSELLOR

        if commit:
            user.save()

            CounsellorProfile.objects.create(
                user=user,
                professional_title=self.cleaned_data["professional_title"],
                specialization=self.cleaned_data["specialization"],
                years_of_experience=self.cleaned_data["years_of_experience"],
                license_number=self.cleaned_data["license_number"],
                qualifications=self.cleaned_data["qualifications"],
                bio=self.cleaned_data["bio"],
                profile_photo=self.cleaned_data["profile_photo"],
                license_document=self.cleaned_data["license_document"],
            )

        return user

        self.fields["profile_photo"].widget.attrs.update({
            "class": "form-control"
        })

        self.fields["license_document"].widget.attrs.update({
            "class": "form-control"
        })

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"
        })
    )

