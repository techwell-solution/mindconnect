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

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    professional_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    specialization = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    years_of_experience = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    license_number = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    qualifications = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
        })
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
        })
    )

    profile_photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control",
        })
    )

    license_document = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control",
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
        })
    )

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
            "bio": "Tell clients about yourself...",
            "password1": "Password",
            "password2": "Confirm Password",
        }

        for name, field in self.fields.items():
            if name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[name]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone_number = self.cleaned_data["phone_number"]
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

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            "profile_photo",
            "date_of_birth",
            "gender",
            "emergency_contact",
            "emergency_phone",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date"}
            )
        }
