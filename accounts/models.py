from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    CLIENT = "client"
    COUNSELLOR = "counsellor"

    ROLE_CHOICES = [
        (CLIENT, "Client"),
        (COUNSELLOR, "Counsellor"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CLIENT,
    )

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    is_verified = models.BooleanField(default=False)


    @property
    def profile(self):
        if self.role == self.CLIENT:
            return self.client_profile
        return self.counsellor_profile

    def __str__(self):
        return self.get_full_name() or self.username


class ClientProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="client_profile"
    )

    profile_photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
        ("Prefer not to say", "Prefer not to say"),
    ]

    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        blank=True
    )

    emergency_contact = models.CharField(
        max_length=100,
        blank=True
    )

    emergency_phone = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return f"{self.user.get_full_name()} - Client"


class CounsellorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="counsellor_profile"
    )

    professional_title = models.CharField(max_length=100)

    specialization = models.CharField(max_length=100)

    years_of_experience = models.PositiveIntegerField(default=0)

    license_number = models.CharField(max_length=100)

    qualifications = models.TextField()

    bio = models.TextField(blank=True)

    profile_photo = models.ImageField(
        upload_to="counsellors/",
        blank=True,
        null=True
    )

    license_document = models.FileField(
        upload_to="licenses/",
        blank=True,
        null=True
    )

    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} - Counsellor"