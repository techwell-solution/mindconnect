from django.urls import path
from .views import home, about, services, service_detail, case_study

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path("services/<slug:slug>/", service_detail, name="service_detail"),
    path('case_study/', case_study, name='case_study'),
]






