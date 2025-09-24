from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import TreatmentCategory, Treatment


def treatments_home(request: HttpRequest) -> HttpResponse:
    categories = TreatmentCategory.objects.all().order_by("type", "name")  # type: ignore
    return render(request, "treatments/home.html", {"categories": categories})


def treatment_detail(request: HttpRequest, slug: str) -> HttpResponse:
    treatment = get_object_or_404(Treatment, slug=slug)
    hospitals = treatment.hospitals.all()[:5]
    doctors = treatment.doctors.all()[:5]
    faqs = treatment.faqs.all()
    return render(
        request,
        "treatments/detail.html",
        {"treatment": treatment, "hospitals": hospitals, "doctors": doctors, "faqs": faqs},
    )

# Create your views here.