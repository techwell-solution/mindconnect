from django.urls import path

from . import views


urlpatterns = [
    path("session/<int:session_id>/", views.payment_options, name="payment_options",),
    path("paystack/<int:session_id>/initialize/", views.paystack_initialize, name="paystack_initialize",),
    path("paystack/callback/", views.paystack_callback,  name="paystack_callback",),
    path("success/<int:payment_id>/", views.payment_success, name="payment_success",),
    path("failed/<int:payment_id>/", views.payment_failed, name="payment_failed",),
    path("paystack/webhook/", views.paystack_webhook,  name="paystack_webhook",),
    path("paypal/create/<int:session_id>/", views.paypal_create_order, name="paypal_create_order",),
    path("paypal/capture/<int:session_id>/", views.paypal_capture_order, name="paypal_capture_order",),
]