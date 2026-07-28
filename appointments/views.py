from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SessionForm, JournalEntryForm, ProgressGoalForm
from django.contrib import messages
from .models import Session, Payment, JournalEntry, ProgressGoal
from accounts.models import ClientProfile
from django.db.models import Sum

# Create your views here.
@login_required
def client_dashboard(request):

    profile, created = ClientProfile.objects.get_or_create(
        user=request.user
    )

    context = {
        "profile": profile,
    }

    return render(
        request,
        "appointments/client_dashboard.html",
        context,
    )


@login_required()
def book_appointment(request):

    if request.method == "POST":

        form = SessionForm(request.POST)

        if form.is_valid():

            appointment = form.save(commit=False)

            appointment.client = request.user

            appointment.save()

            messages.success(
                request,
                "Your appointment request has been submitted successfully."
            )

            return redirect("appointments:appointments")

    else:

        form = SessionForm()

    return render(
        request,
        "appointments/book_appointment.html",
        {
            "form": form,
        },
    )


@login_required()
def appointments(request):

    upcoming_appointments = Session.objects.filter(
        client=request.user
    ).order_by(
        "appointment_date",
        "appointment_time",
    )

    return render(
        request,
        "appointments/appointments.html",
        {
            "upcoming_appointments": upcoming_appointments,
        },
    )

@login_required
def payments(request):

    payments = Payment.objects.filter(
        client=request.user
    ).order_by("-payment_date")

    context = {

        "payment_history": payments.filter(status="paid"),
        "pending_payments": payments.filter(status="pending"),
        "total_paid": payments.filter(status="paid").aggregate(
            total=Sum("amount")
        )["total"] or 0,

        "outstanding_balance": payments.filter(
            status="pending"
        ).aggregate(total=Sum("amount"))["total"] or 0,

        "completed_sessions": payments.filter(
            status="paid"
        ).count(),
    }

    return render(request, "appointments/payments.html", context)

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