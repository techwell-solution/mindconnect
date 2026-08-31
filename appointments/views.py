from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JournalEntryForm, ProgressGoalForm, BookingForm
from django.contrib import messages
from .models import Session,  JournalEntry, ProgressGoal, Booking
from accounts.models import ClientProfile
from django.db.models import Sum
from payments.models import Payment
from django.utils import timezone

# Create your views here.
@login_required
def client_dashboard(request):

    profile, created = ClientProfile.objects.get_or_create(
        user=request.user
    )

    upcoming_appointments = Booking.objects.filter(
        client=request.user,
        status="approved",
    ).order_by(
        "preferred_date",
        "preferred_time",
    )

    next_appointment = upcoming_appointments.first()

    context = {
        "profile": profile,
        "upcoming_appointments": upcoming_appointments,
        "next_appointment": next_appointment,
    }

    return render(
        request,
        "appointments/client_dashboard.html",
        context,
    )
@login_required
def appointments(request):

    today = timezone.localdate()

    upcoming_appointments = Booking.objects.filter(
        client=request.user,
        preferred_date__gte=today,
    ).exclude(
        status__in=["declined", "cancelled"]
    ).order_by(
        "preferred_date",
        "preferred_time",
    )

    past_appointments = Booking.objects.filter(
        client=request.user,
        preferred_date__lt=today,
    ).order_by(
        "-preferred_date",
        "-preferred_time",
    )

    return render(
        request,
        "appointments/appointments.html",
        {
            "upcoming_appointments": upcoming_appointments,
            "past_appointments": past_appointments,
        },
    )

@login_required
def payments(request):

    payments = Payment.objects.filter(
        client=request.user
    ).select_related(
        "session"
    ).order_by(
        "-paid_at",
        "-created_at"
    )

    payment_history = payments.filter(
        status="successful"
    )

    pending_payments = payments.filter(
        status__in=[
            "pending",
            "processing",
        ]
    )

    total_paid = payment_history.aggregate(
        total=Sum("amount")
    )["total"] or 0

    outstanding_balance = pending_payments.aggregate(
        total=Sum("amount")
    )["total"] or 0

    completed_sessions = Session.objects.filter(
        client=request.user,
        status="completed"
    ).count()

    awaiting_payment_sessions = Session.objects.filter(
        client=request.user,
        status="awaiting_payment"
    )

    confirmed_sessions = Session.objects.filter(
        client=request.user,
        status="confirmed"
    )

    context = {
        "payments": payments,
        "payment_history": payment_history,
        "pending_payments": pending_payments,

        "total_paid": total_paid,
        "outstanding_balance": outstanding_balance,
        "completed_sessions": completed_sessions,

        "awaiting_payment_sessions": awaiting_payment_sessions,
        "confirmed_sessions": confirmed_sessions,
    }

    return render(
        request,
        "appointments/payments.html",
        context
    )

@login_required
def journal_list(request):

    journals = JournalEntry.objects.filter(
        user=request.user
    )

    context = {
        "journals": journals,
    }

    return render(
        request,
        "appointments/journal_list.html",
        context,
    )


@login_required
def journal_create(request):

    if request.method == "POST":

        form = JournalEntryForm(request.POST)

        if form.is_valid():

            journal = form.save(commit=False)
            journal.user = request.user
            journal.save()

            messages.success(
                request,
                "Journal entry saved successfully."
            )

            return redirect("journal_list")

    else:

        form = JournalEntryForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "appointments/journal_create.html",
        context,
    )


@login_required
def progress_tracker(request):

    if request.method == "POST":
        form = ProgressGoalForm(request.POST)

        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect("progress_tracker")

    else:
        form = ProgressGoalForm()

    goals = ProgressGoal.objects.filter(user=request.user)

    return render(
        request,
        "appointments/progress_tracker.html",
        {
            "form": form,
            "goals": goals,
        },
    )

@login_required
def session_history(request):
    sessions = (
        Session.objects.filter(
            client=request.user,
            status="completed"
        )
        .select_related("counselor")
        .order_by("-appointment_date", "-appointment_time")
    )

    context = {
        "sessions": sessions,
    }

    return render(request, "appointments/session_history.html", context)

@login_required
def book_session(request):

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            # Automatically assign logged-in client
            booking.client = request.user

            # New booking requests are pending
            booking.status = "pending"

            booking.save()

            messages.success(
                request,
                "Your booking request has been submitted successfully."
            )

            return redirect(
                "booking_confirmation",
                booking_id=booking.id
            )

    else:
        form = BookingForm()

    return render(
        request,
        "appointments/book_session.html",
        {
            "form": form,
        }
    )

@login_required
def booking_confirmation(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        client=request.user,
    )

    return render(
        request,
        "appointments/booking_confirmation.html",
        {
            "booking": booking,
        }
    )