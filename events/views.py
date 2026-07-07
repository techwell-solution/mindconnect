from django.shortcuts import render, get_object_or_404
from .models import Event

# Create your views here.
def events(request):
    events = Event.objects.filter(is_active=True)

    context = {
        "events": events,
    }
    return render(request, "events/events.html", context)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)

    return render(request, "events/event_detail.html", {
        "event": event
    })