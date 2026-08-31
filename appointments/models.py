from django.db import models
from django.conf import settings
from accounts.models import User

# Create your models here.
class Session(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("awaiting_payment", "Awaiting Payment"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    SESSION_TYPES = [
        ("individual", "Individual Therapy"),
        ("couples", "Couples Therapy"),
        ("family", "Family Therapy"),
        ("group", "Group Therapy"),
        ("corporate", "Corporate Therapy"),
    ]

    SESSION_MODES = [
        ("online", "Online"),
        ("physical", "In Person"),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_sessions",
    )

    counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="counselor_sessions",
    )

    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPES,
    )

    session_mode = models.CharField(
        max_length=20,
        choices=SESSION_MODES,
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    duration_minutes = models.PositiveIntegerField(default=60)

    notes = models.TextField(blank=True)

    meeting_link = models.URLField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["appointment_date", "appointment_time"]

    def __str__(self):
        return f"{self.client.get_full_name()} - {self.appointment_date}"



class JournalEntry(models.Model):

    MOOD_CHOICES = [
        ("happy", "😊 Happy"),
        ("calm", "😌 Calm"),
        ("neutral", "😐 Neutral"),
        ("sad", "😔 Sad"),
        ("anxious", "😟 Anxious"),
        ("angry", "😠 Angry"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="journal_entries"
    )

    title = models.CharField(max_length=200)

    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES,
        default="neutral"
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.title}"

from django.db import models
from django.conf import settings

class ProgressGoal(models.Model):
    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progress_goals"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    target_date = models.DateField(null=True, blank=True)

    progress = models.PositiveIntegerField(default=0)  # 0-100

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="not_started"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Booking(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("declined", "Declined"),
        ("cancelled", "Cancelled"),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="booking_requests"
    )

    session = models.OneToOneField(
        Session,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="booking"
    )

    session_type = models.CharField(
        max_length=30,
        choices=Session.SESSION_TYPES
    )

    session_mode = models.CharField(
        max_length=20,
        choices=Session.SESSION_MODES
    )

    preferred_date = models.DateField()

    preferred_time = models.TimeField()

    duration_minutes = models.PositiveIntegerField(default=60)

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client} → {self.counselor}"