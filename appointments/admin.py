from django.contrib import admin
from .models import Session, JournalEntry, ProgressGoal, Booking

# Register your models here.
@admin.action(description="Approve selected bookings")
def approve_bookings(modeladmin, request, queryset):

    for booking in queryset:

        # Don't create another session if one already exists
        if booking.session:
            continue

        session = Session.objects.create(
            client=booking.client,
            counselor=booking.counselor,
            session_type=booking.session_type,
            session_mode=booking.session_mode,
            appointment_date=booking.preferred_date,
            appointment_time=booking.preferred_time,
            duration_minutes=booking.duration_minutes,
            notes=booking.notes,
            status="awaiting_payment",
        )

        booking.session = session
        booking.status = "approved"

        booking.save(
            update_fields=[
                "session",
                "status",
            ]
        )

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "counselor",
        "session_type",
        "session_mode",
        "appointment_date",
        "appointment_time",
        "duration_minutes",
        "status",
    )

    list_filter = (
        "status",
        "session_type",
        "session_mode",
        "appointment_date",
    )

    search_fields = (
        "client__username",
        "client__first_name",
        "client__last_name",
        "counselor__username",
        "counselor__first_name",
        "counselor__last_name",
    )

    ordering = ("-appointment_date", "-appointment_time")


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "mood",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "mood",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "title",
        "content",
    )

    ordering = ("-created_at",)


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

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "counselor",
        "session_type",
        "session_mode",
        "preferred_date",
        "preferred_time",
        "duration_minutes",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "session_type",
        "session_mode",
        "preferred_date",
        "created_at",
    )

    search_fields = (
        "client__username",
        "client__first_name",
        "client__last_name",
        "counselor__username",
        "counselor__first_name",
        "counselor__last_name",
    )

    ordering = ("-created_at",)