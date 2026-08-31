from django.conf import settings
from django.db import models

from appointments.models import Session


class Payment(models.Model):

    GATEWAY_CHOICES = [
        ("paystack", "Paystack"),
        ("paypal", "PayPal"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("successful", "Successful"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    ]

    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=3,
        default="KES",
    )

    gateway = models.CharField(
        max_length=20,
        choices=GATEWAY_CHOICES,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    reference = models.CharField(
        max_length=100,
        unique=True,
    )

    transaction_id = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    gateway_response = models.JSONField(
        blank=True,
        null=True,
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference} - {self.amount} {self.currency}"