import requests
from django.conf import settings
import uuid
from django.db import transaction
from django.utils import timezone
from payments.models import Payment


PAYSTACK_BASE_URL = "https://api.paystack.co"


def initialize_paystack_payment(
    email,
    amount,
    reference,
    callback_url,
):
    """
    Initialize a Paystack transaction.

    Paystack expects the amount in the smallest
    currency unit, so KES 2,000 becomes 200000.
    """

    url = f"{PAYSTACK_BASE_URL}/transaction/initialize"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "email": email,
        "amount": int(amount * 100),
        "currency": "KES",
        "reference": reference,
        "callback_url": callback_url,
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

def generate_payment_reference():
    return f"MC-{uuid.uuid4().hex[:12].upper()}"

def verify_paystack_payment(reference):
    """
    Verify a Paystack transaction using its reference.
    """

    url = f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

def complete_payment(
    payment,
    transaction_id,
    gateway_response,
):
    """
    Mark a payment as successful and confirm
    the associated session.

    This function is idempotent.
    """

    with transaction.atomic():

        payment = (
            Payment.objects
            .select_for_update()
            .select_related("session")
            .get(pk=payment.pk)
        )

        # Already completed
        if payment.status == "successful":
            return payment

        payment.status = "successful"

        payment.transaction_id = str(
            transaction_id
        )

        payment.gateway_response = (
            gateway_response
        )

        payment.paid_at = timezone.now()

        payment.save(
            update_fields=[
                "status",
                "transaction_id",
                "gateway_response",
                "paid_at",
            ]
        )

        session = payment.session

        if session.status == "awaiting_payment":

            session.status = "confirmed"

            session.save(
                update_fields=["status"]
            )

        return payment