from django.urls import path
from .views import(
    assessments,
    assessment_list,
    assessment_detail,
    assessment_result,
    phq9_assessment, 
    phq9_result,
    gad7_assessment, 
    gad7_result,
    stress_assessment,
    stress_result
)

urlpatterns = [
    path("assessments/", assessments, name="assessments"),
    path("list/", assessment_list, name="assessment_list"),
    path("<int:pk>/", assessment_detail, name="assessment_detail"),
    path("result/<int:pk>/", assessment_result, name="assessment_result"),
    path("phq9/", phq9_assessment, name="phq9", ),
    path("phq9/<int:pk>/", phq9_result, name="phq9_result", ),
    path("gad7/", gad7_assessment, name="gad7_assessment", ),
    path("gad7/result/<int:pk>/", gad7_result,  name="gad7_result", ),
    path( "stress/",  stress_assessment, name="stress_assessment" ),
    path("stress/result/<int:assessment_id>/", stress_result,  name="stress_result" ),
]