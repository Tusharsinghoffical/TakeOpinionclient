from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from treatments.models import Treatment
from hospitals.models import Hospital
from doctors.models import Doctor
from blogs.models import BlogPost
from .models import Country


def home(request: HttpRequest) -> HttpResponse:
    context = {
        "top_treatments": Treatment.objects.all()[:6],
        "top_hospitals": Hospital.objects.all()[:4],
        "top_doctors": Doctor.objects.all()[:4],
        "latest_blogs": BlogPost.objects.all()[:3],
    }
    return render(request, "core/home.html", context)


def countries(request: HttpRequest) -> HttpResponse:
    countries_qs = Country.objects.prefetch_related("states").all()
    return render(request, "core/countries.html", {"countries": countries_qs})


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "core/contact.html")


def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "core/privacy.html")


def terms(request: HttpRequest) -> HttpResponse:
    return render(request, "core/terms.html")

# Create your views here.
