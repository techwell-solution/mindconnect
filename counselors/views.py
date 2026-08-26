from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from appointments.models import Session
from accounts.models import User
from django.utils import timezone
from django.contrib import messages
from .models import SessionNote, CounsellorProfile
from .forms import SessionNoteForm

# Create your views here.
@login_required
def counsellor_dashboard(request):

    counsellor = request.user

    sessions = Session.objects.filter(counselor=counsellor)

    context = {
        "total_clients": sessions.values("client").distinct().count(),
        "today_sessions": sessions.filter(status="confirmed").count(),
        "pending_sessions": sessions.filter(status="pending").count(),
        "appointments": sessions.order_by("appointment_date")[:5],
    }

    return render(request, "counselors/counselor_dashboard.html", context)

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