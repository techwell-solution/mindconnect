from django.contrib import admin
from . models import Services, CaseStudy
# Register your models here.
@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_featured",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_featured",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_featured",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_featured",
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
        "short_description",
        "client_profile",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = (
        "created_at",
    )

    list_editable = (
        "is_featured",
        "is_active",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "title",
                "slug",
                "short_description",
                "description",
                "image",
                "icon",
            )
        }),
        ("Case Study Details", {
            "fields": (
                "client_profile",
                "challenge",
                "approach",
                "outcome",
            )
        }),
        ("Status", {
        "fields": (
            "status",       
            "is_featured",
            "is_active",
            "created_at",
        )
    }),
    )
