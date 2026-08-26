from django.db import models
from django.conf import settings
from appointments.models import Session

# Create your models here.
class SessionNote(models.Model):
    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
        related_name="session_note"
    )

    counsellor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="session_notes"
    )

    diagnosis = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    observations = models.TextField()

    interventions = models.TextField(
        blank=True,
        null=True
    )

    recommendations = models.TextField(
        blank=True,
        null=True
    )

    next_session_plan = models.TextField(
        blank=True,
        null=True
    )

    is_private = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.session.client.get_full_name()} - {self.session.appointment_date}"

class CounsellorProfile(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=255)

    photo = models.ImageField(
        upload_to="counsellors/",
        blank=True,
        null=True
    )

    short_bio = models.TextField(
        blank=True,
        default="",
        help_text="Short introduction displayed on the homepage."
    )

    bio = models.TextField(
        help_text="Full biography displayed on the About Us page."
    )

    specializations = models.TextField(
        help_text="Enter one specialization per line."
    )

    experience = models.TextField()

    qualifications = models.TextField(
        help_text="Enter one qualification per line."
    )

    approach = models.TextField()

    years_experience = models.PositiveIntegerField(default=0)

    online_support = models.BooleanField(default=True)
    in_person_support = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Counsellor Profile"
        verbose_name_plural = "Counsellor Profile"

    def __str__(self):
        return self.name

    @property
    def specialization_list(self):
        return [
            item.strip()
            for item in self.specializations.splitlines()
            if item.strip()
        ]

    @property
    def qualification_list(self):
        return [
            item.strip()
            for item in self.qualifications.splitlines()
            if item.strip()
        ]