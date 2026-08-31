from decimal import Decimal, InvalidOperation
import hashlib
import hmac
import json
import requests
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from appointments.models import Session
from .models import Payment
from django.urls import reverse
from .paypal import create_paypal_order, capture_paypal_order, convert_kes_to_usd
from .services import (
    generate_payment_reference,
    initialize_paystack_payment,
)


@login_required
def payment_options(request, session_id):

    session = get_object_or_404(
        Session,
        id=session_id,
        client=request.user,
    )

    if session.status != "awaiting_payment":
        return redirect("client_dashboard")

    return render(
        request,
        "payments/payment_options.html",
        {
            "session": session,
            "paypal_client_id": settings.PAYPAL_CLIENT_ID,
        },
    )


@login_required
def paystack_initialize(request, session_id):

    session = get_object_or_404(
        Session,
        id=session_id,
        client=request.user,
    )

    if session.status != "awaiting_payment":
        return redirect("client_dashboard")

    if request.method != "POST":
        return redirect(
            "payment_options",
            session_id=session.id,
        )

    # Get amount entered by client
    amount_input = request.POST.get("amount", "").strip()

    try:
        amount = Decimal(amount_input)

    except (InvalidOperation, ValueError):
        return render(
            request,
            "payments/payment_options.html",
            {
                "session": session,
                "error": "Please enter a valid amount.",
            },
        )

    if amount <= 0:
        return render(
            request,
            "payments/payment_options.html",
            {
                "session": session,
                "error": "Payment amount must be greater than zero.",
            },
        )

    # Create a fresh reference for every initialization attempt
    reference = generate_payment_reference()

    # Because Payment.session is OneToOneField,
    # reuse the existing payment instead of creating another one.
    payment = Payment.objects.filter(
        session=session
    ).first()

    if payment:
        payment.client = request.user
        payment.amount = amount
        payment.currency = "KES"
        payment.gateway = "paystack"
        payment.status = "pending"
        payment.reference = reference

        payment.save(
            update_fields=[
                "client",
                "amount",
                "currency",
                "gateway",
                "status",
                "reference",
                "updated_at",
            ]
        )

    else:
        payment = Payment.objects.create(
            session=session,
            client=request.user,
            amount=amount,
            currency="KES",
            gateway="paystack",
            status="pending",
            reference=reference,
        )

    callback_url = request.build_absolute_uri(
        reverse("paystack_callback")
    )

    try:
        response = initialize_paystack_payment(
            email=request.user.email,
            amount=payment.amount,
            reference=payment.reference,
            callback_url=callback_url,
        )

        print("PAYSTACK RESPONSE:", response)

        if (
            response.get("status") is True
            and response.get("data")
            and response["data"].get("authorization_url")
        ):
            payment.status = "processing"
            payment.gateway_response = response

            payment.save(
                update_fields=[
                    "status",
                    "gateway_response",
                    "updated_at",
                ]
            )

            return redirect(
                response["data"]["authorization_url"]
            )

        # Paystack returned an error
        payment.status = "failed"
        payment.gateway_response = response

        payment.save(
            update_fields=[
                "status",
                "gateway_response",
                "updated_at",
            ]
        )

        return render(
            request,
            "payments/payment_options.html",
            {
                "session": session,
                "error": response.get(
                    "message",
                    "Paystack could not initialize the payment.",
                ),
            },
        )

    except Exception as e:

        print("PAYSTACK ERROR:", repr(e))

        payment.status = "failed"
        payment.gateway_response = {
            "error": str(e),
        }

        payment.save(
            update_fields=[
                "status",
                "gateway_response",
                "updated_at",
            ]
        )

        return render(
            request,
            "payments/payment_options.html",
            {
                "session": session,
                "error": f"Paystack error: {str(e)}",
            },
        )
def verify_paystack_payment(reference):

    url = (
        f"https://api.paystack.co/transaction/verify/"
        f"{reference}"
    )

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    return response.json()

@login_required
def paystack_callback(request):

    reference = request.GET.get("reference")

    if not reference:
        return redirect("client_dashboard")

    payment = get_object_or_404(
        Payment,
        reference=reference,
        client=request.user,
    )

    try:

        response = verify_paystack_payment(
            reference=payment.reference
        )

        if (
            response.get("status")
            and response.get("data", {}).get("status") == "success"
        ):

            payment.status = "successful"
            payment.transaction_id = response["data"].get(
                "id"
            )
            payment.gateway_response = response
            payment.paid_at = timezone.now()

            payment.save(
                update_fields=[
                    "status",
                    "transaction_id",
                    "gateway_response",
                    "paid_at",
                    "updated_at",
                ]
            )

            # Confirm the session
            session = payment.session

            session.status = "confirmed"

            session.save(
                update_fields=[
                    "status",
                ]
            )

            messages.success(
                request,
                "Payment successful. Your counselling session is now confirmed.",
            )

            return redirect("client_appointments")

        # Payment verification failed
        payment.status = "failed"
        payment.gateway_response = response

        payment.save(
            update_fields=[
                "status",
                "gateway_response",
                "updated_at",
            ]
        )

        messages.error(
            request,
            "Payment could not be verified.",
        )

    except Exception as e:

        payment.status = "failed"
        payment.gateway_response = {
            "error": str(e),
        }

        payment.save(
            update_fields=[
                "status",
                "gateway_response",
                "updated_at",
            ]
        )

        messages.error(
            request,
            "Unable to verify payment.",
        )

    return redirect("appointments")

@login_required
def payment_success(request, payment_id):

    payment = get_object_or_404(
        Payment,
        id=payment_id,
        client=request.user,
        status="successful",
    )

    return render(
        request,
        "payments/payment_success.html",
        {
            "payment": payment,
            "session": payment.session,
        },
    )

@login_required
def payment_failed(request, payment_id):

    payment = get_object_or_404(
        Payment,
        id=payment_id,
        client=request.user,
    )

    return render(request, "payments/payment_failed.html",{
            "payment": payment,
            "session": payment.session,
        },)

@require_POST
def paystack_webhook(request):

    # Get Paystack signature
    signature = request.headers.get("x-paystack-signature")

    if not signature:
        return JsonResponse(
            {"detail": "Missing signature"},
            status=400,
        )

    # Calculate our own signature
    expected_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode("utf-8"),
        request.body,
        hashlib.sha512,
    ).hexdigest()

    # Compare signatures securely
    if not hmac.compare_digest(
        signature,
        expected_signature,
    ):
        return JsonResponse(
            {"detail": "Invalid signature"},
            status=401,
        )

    # Parse webhook payload
    try:
        payload = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse(
            {"detail": "Invalid JSON"},
            status=400,
        )

    event = payload.get("event")
    data = payload.get("data", {})

    # We only need successful payments for now
    if event != "charge.success":
        return JsonResponse(
            {"status": "ignored"},
            status=200,
        )

    reference = data.get("reference")

    if not reference:
        return JsonResponse(
            {"detail": "Missing payment reference"},
            status=400,
        )

    try:
        with transaction.atomic():

            payment = (
                Payment.objects
                .select_for_update()
                .select_related("session")
                .get(
                    reference=reference,
                    gateway="paystack",
                )
            )

            # Idempotency:
            # If this payment has already been processed,
            # don't process it again.
            if payment.status == "successful":
                return JsonResponse(
                    {"status": "already_processed"},
                    status=200,
                )

            # Amount verification
            expected_amount = int(
                payment.amount * 100
            )

            received_amount = data.get("amount")

            if received_amount != expected_amount:
                payment.status = "failed"

                payment.gateway_response = payload

                payment.save(
                    update_fields=[
                        "status",
                        "gateway_response",
                    ]
                )

                return JsonResponse(
                    {"detail": "Amount mismatch"},
                    status=400,
                )

            # Currency verification
            received_currency = data.get("currency")

            if received_currency != payment.currency:
                payment.status = "failed"

                payment.gateway_response = payload

                payment.save(
                    update_fields=[
                        "status",
                        "gateway_response",
                    ]
                )

                return JsonResponse(
                    {"detail": "Currency mismatch"},
                    status=400,
                )

            # Mark payment successful
            payment.status = "successful"

            payment.transaction_id = str(
                data.get("id")
            )

            payment.gateway_response = payload

            payment.paid_at = timezone.now()

            payment.save(
                update_fields=[
                    "status",
                    "transaction_id",
                    "gateway_response",
                    "paid_at",
                ]
            )

            # Confirm session
            session = payment.session

            if session.status == "awaiting_payment":

                session.status = "confirmed"

                session.save(
                    update_fields=["status"]
                )

    except Payment.DoesNotExist:

        return JsonResponse(
            {"detail": "Payment not found"},
            status=404,
        )

    return JsonResponse( {"status": "success"}, status=200,)

@login_required
@require_POST
def paypal_create_order(request, session_id):

    session = get_object_or_404(
        Session,
        id=session_id,
        client=request.user,
    )

    if session.status != "awaiting_payment":
        return JsonResponse(
            {
                "error": "This session is not awaiting payment."
            },
            status=400,
        )

    # --------------------------------
    # Read request body safely
    # --------------------------------

    print("PAYPAL REQUEST BODY:", request.body)

    amount = request.POST.get("amount")

    print("PAYPAL AMOUNT:", amount)

    if not amount:
        return JsonResponse(
            {
                "error": "Payment amount is required."
            },
            status=400,
        )
    # --------------------------------
    # Get amount
    # --------------------------------

    amount = request.POST.get("amount")

    print("PAYPAL AMOUNT:", amount)

    if not amount:
        return JsonResponse(
            {
                "error": "Payment amount is required."
            },
            status=400,
        )

    try:
        amount = Decimal(str(amount))

    except (InvalidOperation, ValueError):
        return JsonResponse(
            {
                "error": "Invalid payment amount."
            },
            status=400,
        )

    if amount <= 0:
        return JsonResponse(
            {
                "error": "Payment amount must be greater than zero."
            },
            status=400,
        )

    # --------------------------------
    # Convert KES → USD
    # --------------------------------

    usd_amount = amount * settings.KES_TO_USD_RATE
    usd_amount = usd_amount.quantize(
    Decimal("0.01")
)

    

    print("KES AMOUNT:", amount)
    print("USD AMOUNT:", usd_amount)

    # --------------------------------
    # Get PayPal access token
    # --------------------------------

    try:

        auth_response = requests.post(
            f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=(
                settings.PAYPAL_CLIENT_ID,
                settings.PAYPAL_CLIENT_SECRET,
            ),
            headers={
                "Accept": "application/json",
                "Accept-Language": "en_US",
            },
            data={
                "grant_type": "client_credentials"
            },
            timeout=30,
        )

        print(
            "PAYPAL AUTH STATUS:",
            auth_response.status_code
        )

        print(
            "PAYPAL AUTH RESPONSE:",
            auth_response.text
        )

        if auth_response.status_code != 200:
            return JsonResponse(
                {
                    "error": "PayPal authentication failed.",
                    "details": auth_response.text,
                },
                status=400,
            )

        access_token = auth_response.json()["access_token"]

    except Exception as e:

        print("PAYPAL AUTH ERROR:", str(e))

        return JsonResponse(
            {
                "error": "Unable to authenticate with PayPal."
            },
            status=400,
        )

    # --------------------------------
    # Create PayPal order
    # --------------------------------

    try:

        paypal_response = requests.post(
            f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders",

            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },

            json={
                "intent": "CAPTURE",

                "purchase_units": [
                    {
                        "reference_id": str(session.id),

                        "description": (
                            f"MindConnect counselling "
                            f"session #{session.id}"
                        ),

                        "amount": {
                            "currency_code": "USD",
                            "value": str(usd_amount),
                        },
                    }
                ],
            },

            timeout=30,
        )

        print(
            "PAYPAL ORDER STATUS:",
            paypal_response.status_code
        )

        print(
            "PAYPAL ORDER RESPONSE:",
            paypal_response.text
        )

        if paypal_response.status_code not in [200, 201]:

            return JsonResponse(
                {
                    "error": "PayPal order creation failed.",
                    "details": paypal_response.text,
                },
                status=400,
            )

        order_data = paypal_response.json()

        return JsonResponse(
            {
                "id": order_data["id"]
            }
        )

    except Exception as e:

        print("PAYPAL ORDER ERROR:", str(e))

        return JsonResponse(
            {
                "error": "Unable to create PayPal order."
            },
            status=400,
        )
@login_required
@require_POST
def paypal_capture_order(request, session_id):

    session = get_object_or_404(
        Session,
        id=session_id,
        client=request.user,
    )

    try:
        data = json.loads(request.body)

        order_id = data.get("orderID")

        if not order_id:
            return JsonResponse(
                {
                    "error": "PayPal order ID is required."
                },
                status=400,
            )

        # Get PayPal access token
        auth_response = requests.post(
            f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=(
                settings.PAYPAL_CLIENT_ID,
                settings.PAYPAL_CLIENT_SECRET,
            ),
            headers={
                "Accept": "application/json",
                "Accept-Language": "en_US",
            },
            data={
                "grant_type": "client_credentials"
            },
            timeout=30,
        )

        auth_response.raise_for_status()

        access_token = auth_response.json()["access_token"]

        # Capture payment
        capture_response = requests.post(
            f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            timeout=30,
        )

        print(
            "PAYPAL CAPTURE STATUS:",
            capture_response.status_code
        )

        print(
            "PAYPAL CAPTURE RESPONSE:",
            capture_response.text
        )

        if capture_response.status_code not in [200, 201]:

            return JsonResponse(
                {
                    "error": "PayPal payment capture failed.",
                    "details": capture_response.text,
                },
                status=400,
            )

        capture_data = capture_response.json()

        # Make sure PayPal actually completed the payment
        if capture_data.get("status") == "COMPLETED":

            session.status = "confirmed"
            session.save(update_fields=["status"])

            return JsonResponse(
                {
                    "success": True,
                    "redirect_url": reverse(
                        "payment_success",
                        args=[session.id],
                    ),
                }
            )

        return JsonResponse(
            {
                "error": "Payment was not completed.",
                "details": capture_data,
            },
            status=400,
        )

    except Exception as e:

        print("PAYPAL CAPTURE ERROR:", str(e))

        return JsonResponse(
            {
                "error": str(e)
            },
            status=400,
        )

