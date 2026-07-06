from django.urls import path
from .views import home, about, services, service_detail, case_study, case_study_detail

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path("services/<slug:slug>/", service_detail, name="service_detail"),
    path("case-studies/", case_study, name="case_study", ),
    path("case-studies/<slug:slug>/", case_study_detail, name="case_study_detail",),
]






