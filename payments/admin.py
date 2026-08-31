from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "reference",
        "client",
        "session",
        "amount",
        "currency",
        "gateway",
        "status",
        "paid_at",
        "created_at",
    )

    list_filter = (
        "gateway",
        "status",
        "currency",
        "created_at",
    )

    search_fields = (
        "reference",
        "transaction_id",
        "client__username",
        "client__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "paid_at",
        "gateway_response",
    )

    ordering = ("-created_at",)
