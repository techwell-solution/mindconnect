from django.urls import path
from .views import (
    client_dashboard,
    appointments,
    book_appointment,
    payments,
    journal_list,
    journal_create,
    progress_tracker,
    session_history
)

urlpatterns = [
    path( "dashboard/client/",  client_dashboard, name="client_dashboard", ),
    path("appointments/", appointments, name="appointments", ),
    path("appointments/book/", book_appointment, name="booking", ),
    path("payments/", payments, name="payments"),
    path("journal/", journal_list, name="journal_list", ),
    path("journal/new/", journal_create, name="journal_create" ),
    path("progress/", progress_tracker, name="progress_tracker",),
    path( "session-history/", session_history,  name="session_history",),
]