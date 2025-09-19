from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Doctor


def doctors_list(request: HttpRequest) -> HttpResponse:
    doctors = Doctor.objects.all()
    return render(request, "doctors/list.html", {"doctors": doctors})


def doctor_detail(request: HttpRequest, slug: str) -> HttpResponse:
    doctor = get_object_or_404(Doctor, slug=slug)
    return render(request, "doctors/detail.html", {"doctor": doctor})

# Create your views here.
