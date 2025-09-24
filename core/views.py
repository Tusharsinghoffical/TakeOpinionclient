from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
import os
from treatments.models import Treatment
from hospitals.models import Hospital
from doctors.models import Doctor
from blogs.models import BlogPost
from typing import Any


def home(request: HttpRequest) -> HttpResponse:
    context: dict[str, Any] = {
        "top_treatments": Treatment.objects.all()[:6],  # type: ignore
        "top_hospitals": Hospital.objects.all()[:4],  # type: ignore
        "top_doctors": Doctor.objects.all()[:4],  # type: ignore
        "latest_blogs": BlogPost.objects.all()[:3],  # type: ignore
    }
    return render(request, "core/home.html", context)


def search(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q', '')
    treatments = []
    doctors = []
    hospitals = []
    blog_posts = []
    
    if query:
        # Search treatments by name and description
        treatments = list(Treatment.objects.filter(name__icontains=query) | Treatment.objects.filter(description__icontains=query))  # type: ignore
        
        # Search doctors by name and key_points
        doctors = list(Doctor.objects.filter(name__icontains=query) | Doctor.objects.filter(key_points__icontains=query))  # type: ignore
        
        # Search hospitals by name and about
        hospitals = list(Hospital.objects.filter(name__icontains=query) | Hospital.objects.filter(about__icontains=query))  # type: ignore
        
        # Search blog posts by title and content
        blog_posts = list(BlogPost.objects.filter(title__icontains=query) | BlogPost.objects.filter(content__icontains=query))  # type: ignore
    
    context = {
        'query': query,
        'treatments': treatments,
        'doctors': doctors,
        'hospitals': hospitals,
        'blog_posts': blog_posts,
        'total_results': len(treatments) + len(doctors) + len(hospitals) + len(blog_posts)
    }
    
    return render(request, "core/search_results.html", context)


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "core/contact.html")


def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "core/privacy.html")


def terms(request: HttpRequest) -> HttpResponse:
    return render(request, "core/terms.html")


@require_http_methods(["GET"])
def health_check(request: HttpRequest) -> HttpResponse:
    return HttpResponse(b"OK")


@require_http_methods(["GET"])
def static_files_check(request: HttpRequest) -> HttpResponse:
    # Check if static files directory exists
    static_root = getattr(settings, "STATIC_ROOT", None)
    if static_root and os.path.exists(static_root):
        return HttpResponse(b"Static files directory exists")
    else:
        return HttpResponse(b"Static files directory not found", status=500)