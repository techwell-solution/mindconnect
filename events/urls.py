from django.urls import path
from .views import events, event_detail

urlpatterns = [
    path('events/', events, name='events'),
    path("events/<slug:slug>/", event_detail, name="event_detail"),
]