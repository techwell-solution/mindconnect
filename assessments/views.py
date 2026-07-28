from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PHQ9Form, GAD7Form, StressAssessmentForm
from .models import PHQ9Assessment, GAD7Assessment, StressAssessment

# Create your views here.
def assessments(request):
    return render(request, "assessments/assessments.html")


def assessment_list(request):
    return render(request, "assessments/assessment_list.html")


def assessment_detail(request, pk):
    return render(request, "assessments/assessment_detail.html")


def assessment_result(request, pk):
    return render(request, "assessments/result.html")


@login_required
def phq9_assessment(request):

    if request.method == "POST":

        form = PHQ9Form(request.POST)

        if form.is_valid():

            assessment = form.save(commit=False)
            assessment.user = request.user
            assessment.save()

            return redirect(
                "phq9_result",
                assessment.id
            )

    else:
        form = PHQ9Form()

    return render(
        request,
        "assessments/phq9.html",
        {
            "form": form
        }
    )


@login_required
def phq9_result(request, pk):
    assessment = get_object_or_404 (PHQ9Assessment, pk=pk, user=request.user )
    return render(request,"assessments/phq9_result.html",{"assessment": assessment }
    )

@login_required
def phq9_assessment(request):

    if request.method == "POST":

        form = PHQ9Form(request.POST)

        if form.is_valid():

            assessment = form.save(commit=False)
            assessment.user = request.user
            assessment.save()

            return redirect(
                "phq9_result",
                assessment.id
            )

    else:
        form = PHQ9Form()

    return render(
        request,
        "assessments/phq9.html",
        {
            "form": form
        }
    )

@login_required
def phq9_result(request, pk):

    assessment = get_object_or_404(
        PHQ9Assessment,
        pk=pk,
        user=request.user
    )

    return render(
        request,
        "assessments/phq9_result.html",
        {
            "assessment": assessment
        }
    )

@login_required
def gad7_assessment(request):
    if request.method == "POST":
        form = GAD7Form(request.POST)

        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.user = request.user
            assessment.save()

            return redirect(
                "gad7_result",
                assessment.id
            )

    else:
        form = GAD7Form()

    return render(
        request,
        "assessments/gad7_assessment.html",
        {"form": form},
    )


@login_required
def gad7_result(request, pk):
    assessment = get_object_or_404(
        GAD7Assessment,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "assessments/gad7_result.html",
        {
            "assessment": assessment,
        },
    )

@login_required
def stress_assessment(request):
    if request.method == "POST":
        form = StressAssessmentForm(request.POST)

        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.user = request.user
            assessment.save()

            return redirect(
                "stress_result",
                assessment_id=assessment.id
            )
    else:
        form = StressAssessmentForm()

    return render(
        request,
        "assessments/stress_assessment.html",
        {"form": form}
    )

@login_required
def stress_result(request, assessment_id):
    assessment = get_object_or_404(
        StressAssessment,
        id=assessment_id,
        user=request.user
    )

    return render(
        request,
        "assessments/stress_result.html",
        {
            "assessment": assessment
        }
    )