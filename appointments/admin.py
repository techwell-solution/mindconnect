from django.contrib import admin
from .models import ProgressGoal

# Register your models here.
@admin.register(ProgressGoal)
class ProgressGoalAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "progress",
        "status",
        "target_date",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "user__username",
        "user__email",
    )

    ordering = ("-created_at",)