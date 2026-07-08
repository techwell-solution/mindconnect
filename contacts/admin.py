from django.contrib import admin
from .models import Contact
from django.utils.html import format_html

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "subject",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "full_name",
        "email",
        "subject",
        "message",
    )

    list_editable = ("status",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Contact Information", {
            "fields": (
                "full_name",
                "email",
                "phone",
            )
        }),
        ("Message", {
            "fields": (
                "subject",
                "message",
            )
        }),
        ("Management", {
            "fields": (
                "status",
                "created_at",
                "updated_at",
            )
        }),
    )