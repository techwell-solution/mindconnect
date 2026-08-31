from django.urls import path
from .views import (
    client_dashboard,
    appointments,
    payments,
    journal_list,
    journal_create,
    progress_tracker,
    session_history, 
    booking_confirmation, 
    book_session
)

urlpatterns = [
    path( "dashboard/client/",  client_dashboard, name="client_dashboard", ),
    path("appointments/", appointments, name="appointments", ),
    path("payments/", payments, name="payments"),
    path("journal/", journal_list, name="journal_list", ),
    path("journal/new/", journal_create, name="journal_create" ),
    path("progress/", progress_tracker, name="progress_tracker",),
    path( "session-history/", session_history,  name="session_history",),
    path("book/", book_session, name="book_session"),
    path("book/confirmation/<int:booking_id>/", booking_confirmation, name="booking_confirmation"),
]