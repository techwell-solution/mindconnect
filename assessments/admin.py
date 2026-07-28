from django.contrib import admin
from .models import PHQ9Assessment, GAD7Assessment

# Register your models here.
@admin.register(PHQ9Assessment)
class PHQ9AssessmentAdmin(admin.ModelAdmin):
    list_display = ("user", "total_score", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username",)

@admin.register(GAD7Assessment)
class GAD7AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "total_score",
        "interpretation",
        "created_at",
    )

    list_filter = (
        "interpretation",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "total_score",
        "interpretation",
        "created_at",
    )