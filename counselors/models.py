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