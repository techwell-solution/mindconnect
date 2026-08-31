from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from appointments.models import Session
from accounts.models import User
from django.utils import timezone
from django.contrib import messages
from .models import SessionNote, CounsellorProfile
from .forms import SessionNoteForm
from appointments.models import Booking

# Create your views here.

@login_required
def counselor_dashboard(request):

    today = timezone.localdate()

    # =====================================================
    # PENDING BOOKING REQUESTS
    # =====================================================

    pending_bookings = (
        Booking.objects
        .filter(
            counselor=request.user,
            status="pending"
        )
        .select_related("client")
        .order_by("-created_at")
    )

    # =====================================================
    # APPROVED BOOKINGS
    # =====================================================

    approved_bookings = (
        Booking.objects
        .filter(
            counselor=request.user,
            status="approved"
        )
        .select_related(
            "client",
            "session"
        )
        .order_by(
            "preferred_date",
            "preferred_time"
        )
    )

    # =====================================================
    # ALL SESSIONS
    # =====================================================

    sessions = (
        Session.objects
        .filter(
            counselor=request.user
        )
        .select_related("client")
        .order_by(
            "appointment_date",
            "appointment_time"
        )
    )

    # =====================================================
    # UPCOMING SESSIONS
    # =====================================================

    upcoming_sessions = sessions.filter(
        appointment_date__gte=today,
        status__in=[
            "awaiting_payment",
            "confirmed",
        ]
    )

    # =====================================================
    # COMPLETED SESSIONS
    # =====================================================

    completed_sessions = sessions.filter(
        status="completed"
    )

    # =====================================================
    # TOTAL UNIQUE CLIENTS
    # Same logic as client_list
    # =====================================================

    total_clients = (
        sessions
        .values("client")
        .distinct()
        .count()
    )

    # =====================================================
    # TODAY'S CONFIRMED SESSIONS
    # =====================================================

    today_sessions = sessions.filter(
        appointment_date=today,
        status="confirmed"
    ).count()

    # =====================================================
    # PENDING BOOKING REQUESTS COUNT
    # =====================================================

    pending_sessions = pending_bookings.count()

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {
        "pending_bookings": pending_bookings,
        "approved_bookings": approved_bookings,

        "sessions": sessions,
        "upcoming_sessions": upcoming_sessions,
        "completed_sessions": completed_sessions,

        "total_clients": total_clients,
        "today_sessions": today_sessions,
        "pending_sessions": pending_sessions,

        # Your template uses "appointments"
        "appointments": upcoming_sessions,
    }

    return render( request, "counselors/counselor_dashboard.html",  context)

@login_required
def client_list(request):
    clients = (
        Session.objects.filter(counselor=request.user)
        .values(
            "client__id",
            "client__first_name",
            "client__last_name",
            "client__email",
        )
        .annotate(total_sessions=Count("id"))
        .order_by("client__first_name")
    )

    return render(
        request,
        "counselors/client_list.html",
        {"clients": clients},
    )

@login_required
def counsellor_schedule(request):

    sessions = Session.objects.filter(
        counselor=request.user
    ).order_by("appointment_date", "appointment_time")

    today = timezone.now().date()

    context = {
        "sessions": sessions,
        "today_sessions": sessions.filter(
            appointment_date=today
        ).count(),
        "completed_sessions": sessions.filter(
            status="completed"
        ).count(),
        "pending_sessions": sessions.filter(
            status="pending"
        ).count(),
    }

    return render(request,  "counselors/counsellor_schedule.html", context)

@login_required
def session_notes(request):
    notes = SessionNote.objects.filter(
        counsellor=request.user
    ).select_related("session", "session__client")

    context = {
        "notes": notes,
    }

    return render(
        request,
        "counselors/session_notes.html",
        context,
    )

@login_required
def session_note_detail(request, pk):
    note = get_object_or_404(
        SessionNote,
        pk=pk,
        counsellor=request.user,
    )

    return render(
        request,
        "counselors/session_note_detail.html",
        {"note": note},
    )

@login_required
def create_session_note(request, session_id):

    session = get_object_or_404(
        Session,
        id=session_id,
        counselor=request.user,
    )

    # Only allow notes for completed sessions
    if session.status != "completed":
        messages.error(
            request,
            "Session notes can only be created for completed sessions."
        )
        return redirect("session_notes")

    # Prevent duplicate notes
    if hasattr(session, "session_note"):
        messages.warning(
            request,
            "A note already exists for this session."
        )
        return redirect(
            "session_note_detail",
            session.session_note.id,
        )

    if request.method == "POST":
        form = SessionNoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.session = session
            note.counsellor = request.user
            note.save()

            messages.success(
                request,
                "Session note created successfully."
            )

            return redirect("session_notes")

    else:
        form = SessionNoteForm()

    return render(
        request,
        "counselors/session_note_form.html",
        {
            "form": form,
            "session": session,
        },
    )
@login_required
def edit_session_note(request, pk):

    note = get_object_or_404(
        SessionNote,
        pk=pk,
        counsellor=request.user,
    )

    if request.method == "POST":
        form = SessionNoteForm(
            request.POST,
            instance=note,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Session note updated successfully."
            )

            return redirect(
                "session_note_detail",
                note.id,
            )

    else:
        form = SessionNoteForm(instance=note)

    return render(
        request,
        "counselors/session_note_form.html",
        {
            "form": form,
            "note": note,
            "session": note.session,
        },
    )

@login_required
def counsellor_reports(request):
    return render(request, "counselors/counsellor_reports.html")

def counsellor_profile(request):
    counsellor = CounsellorProfile.objects.filter(
        is_active=True
    ).first()

    return render(
        request,
        "counselors/profile.html",
        {
            "counsellor": counsellor,
        }
    )
@login_required
def approve_booking_by_counselor(request, booking_id):

    if request.method != "POST":
        return redirect("counselor_dashboard")

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        counselor=request.user,
        status="pending"
    )

    # Create the session
    session = Session.objects.create(
        client=booking.client,
        counselor=request.user,
        session_type=booking.session_type,
        session_mode=booking.session_mode,
        appointment_date=booking.preferred_date,
        appointment_time=booking.preferred_time,
        duration_minutes=booking.duration_minutes,
        notes=booking.notes,
        status="awaiting_payment",
    )

    # Approve booking
    booking.status = "approved"
    booking.session = session
    booking.save(
        update_fields=[
            "status",
            "session",
        ]
    )

    messages.success(
        request,
        "Booking approved successfully. The client can now make payment."
    )

    return redirect("counselor_dashboard")

@login_required
def decline_booking_by_counselor(request, booking_id):

    if request.method != "POST":
        return redirect("counselor_dashboard")

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        counselor=request.user,
        status="pending"
    )

    booking.status = "declined"

    booking.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        "Booking declined successfully."
    )

    return redirect("counselor_dashboard")