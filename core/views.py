from django.shortcuts import render, get_object_or_404
from .models import Services, CaseStudy, ProcessStep, FAQ
from counselors.models import CounsellorProfile
from testimonials.models import  Testimonial
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    steps = ProcessStep.objects.filter(is_active=True)
    services = Services.objects.filter(
        is_active=True,
        is_featured=True
    )
    counsellor = CounsellorProfile.objects.filter(is_active=True).first()
    testimonials = Testimonial.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by("order")
    faqs = FAQ.objects.filter(is_active=True)
    context = {
        "steps": steps,
        "services": services,
        "counsellor": counsellor,
        "testimonials": testimonials,
         "faqs": faqs,
        }

    return render(request, "core/home.html", context)

def about(request):
    counsellor = CounsellorProfile.objects.filter(
        is_active=True
    ).first()

    context = {
        "counsellor": counsellor,
    }

    return render(request, "core/about.html", context)

def services(request):
    services = Services.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(
            is_active=True,
            is_featured=True
        ).order_by("order")
    faqs = FAQ.objects.filter(is_active=True)
    context = {
        "services": services,
        "testimonials": testimonials,
        "faqs": faqs,
    }
    return render(request, "core/services.html", context)

def service_detail(request, slug):
    service = get_object_or_404(Services, slug=slug)
    return render(request, "core/service_detail.html", {"service": service})

def case_study(request):
    case_studies = CaseStudy.objects.filter(is_active=True, status="published").order_by("-created_at")
    faqs = FAQ.objects.filter(is_active=True)
    context = {
        "case_studies": case_studies,
        "faqs": faqs,
    }
    return render(request, "core/case_study.html", context)

def case_study_detail(request, slug):
    study = get_object_or_404(CaseStudy, slug=slug, is_active=True)
    context = {
        "study": study
    }
    return render(request, "core/case_study_detail.html", context)