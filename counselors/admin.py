from django.contrib import admin
from .models import SessionNote

# Register your models here.
@admin.register(SessionNote)
class SessionNoteAdmin(admin.ModelAdmin):
    list_display = (
        "session",
        "counsellor",
        "created_at",
        "is_private",
    )

    list_filter = (
        "is_private",
        "created_at",
    )

    search_fields = (
        "session__client__first_name",
        "session__client__last_name",
    )