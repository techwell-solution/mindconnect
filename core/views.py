from django.shortcuts import render, get_object_or_404
from .models import Services

# Create your views here.
def home(request):

    services = Services.objects.filter(is_active=True)

    return render(request, "core/home.html",{"services": services})

def about(request):
    return render(request, 'core/about.html')

def services(request):
    services = Services.objects.filter(is_active=True)

    context = {
        "services": services
    }
    return render(request, "core/services.html", context)

def service_detail(request, slug):
    service = get_object_or_404(Services, slug=slug)
    return render(request, "core/service_detail.html", {"service": service})

def case_study(request):
    return render(request, 'core/case_study.html')
