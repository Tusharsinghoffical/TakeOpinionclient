from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
import os
from treatments.models import Treatment
from hospitals.models import Hospital
from doctors.models import Doctor
from blogs.models import BlogPost
from .models import Country
from typing import Any


def home(request: HttpRequest) -> HttpResponse:
    context: dict[str, Any] = {
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


@require_http_methods(["GET"])
def health_check(request: HttpRequest) -> HttpResponse:
    """
    Health check endpoint for Render and other monitoring services.
    Returns a simple 200 OK response.
    """
    return HttpResponse(b"OK", content_type="text/plain", status=200)


@require_http_methods(["GET"])
def static_files_check(request: HttpRequest) -> HttpResponse:
    """
    Static files check endpoint to verify that static files are being served correctly.
    """
    # Check if the logo file exists
    logo_path = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], 'images', 'logo.svg')
    logo_exists = os.path.exists(logo_path)
    
    response_text = f"Static files check:\nLogo file exists: {logo_exists}\nStatic root: {settings.STATIC_ROOT}\nStatic URL: {settings.STATIC_URL}"
    return HttpResponse(response_text.encode(), content_type="text/plain", status=200)