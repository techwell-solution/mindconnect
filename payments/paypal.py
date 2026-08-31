import requests
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP


def get_paypal_access_token():
    url = f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token"

    response = requests.post(
        url,
        auth=(
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_CLIENT_SECRET,
        ),
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
        },
        data={
            "grant_type": "client_credentials",
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["access_token"]


def create_paypal_order(amount, currency="USD"):
    access_token = get_paypal_access_token()

    url = f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders"

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": currency,
                    "value": str(amount),
                }
            }
        ],
    }

    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def capture_paypal_order(order_id):
    access_token = get_paypal_access_token()

    url = (
        f"{settings.PAYPAL_BASE_URL}"
        f"/v2/checkout/orders/{order_id}/capture"
    )

    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        json={},
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

def convert_kes_to_usd(amount_kes):

    amount_kes = Decimal(amount_kes)

    rate = Decimal(
        settings.KES_TO_USD_RATE
    )

    amount_usd = (
        amount_kes * rate
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return amount_usd


def get_paypal_access_token():

    url = (
        f"{settings.PAYPAL_BASE_URL}"
        f"/v1/oauth2/token"
    )

    response = requests.post(
        url,
        auth=(
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_CLIENT_SECRET,
        ),
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
        },
        data={
            "grant_type":
                "client_credentials",
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["access_token"]


def create_paypal_order(
    amount,
    currency="USD",
):

    access_token = (
        get_paypal_access_token()
    )

    url = (
        f"{settings.PAYPAL_BASE_URL}"
        f"/v2/checkout/orders"
    )

    payload = {

        "intent": "CAPTURE",

        "purchase_units": [
            {
                "amount": {
                    "currency_code":
                        currency,

                    "value":
                        str(amount),
                }
            }
        ],
    }

    response = requests.post(
        url,

        headers={
            "Content-Type":
                "application/json",

            "Authorization":
                f"Bearer {access_token}",
        },

        json=payload,

        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def capture_paypal_order(order_id):

    access_token = (
        get_paypal_access_token()
    )

    url = (
        f"{settings.PAYPAL_BASE_URL}"
        f"/v2/checkout/orders/"
        f"{order_id}/capture"
    )

    response = requests.post(
        url,

        headers={
            "Content-Type":
                "application/json",

            "Authorization":
                f"Bearer {access_token}",
        },

        json={},

        timeout=30,
    )

    response.raise_for_status()

    return response.json()