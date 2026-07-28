from django.urls import path
from . import views

urlpatterns = [
    
    path( "dashboard/", views.counsellor_dashboard, name="counselor_dashboard",),
    path("clients/", views.client_list, name="client_list"),
    path("schedule/", views.counsellor_schedule, name="counsellor_schedule" ),
    path("session-notes/", views.session_notes, name="session_notes",),
    path("session-notes/<int:pk>/", views.session_note_detail, name="session_note_detail",),
    path("session/<int:session_id>/notes/add/", views.create_session_note, name="create_session_note",),
    path("session-notes/<int:pk>/edit/", views.edit_session_note, name="edit_session_note", ),
    path("dashboard/reports/", views.counsellor_reports, name="counsellor_reports"),
]