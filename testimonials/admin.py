from django.contrib import admin
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "position",
        "rating",
        "is_featured",
        "is_active",
        "order",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_featured",
        "is_active",
    )

    search_fields = (
        "name",
        "position",
        "message",
    )

    list_editable = (
        "is_featured",
        "is_active",
        "order",
    )

    ordering = (
        "order",
        "-created_at",
    )
