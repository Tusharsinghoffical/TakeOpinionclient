from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
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


@require_http_methods(["GET"])
def get_home_stats(request: HttpRequest) -> JsonResponse:
    """
    Real-time statistics for the home page
    """
    try:
        stats = {
            'treatments_count': Treatment.objects.count(),  # type: ignore
            'hospitals_count': Hospital.objects.count(),  # type: ignore
            'doctors_count': Doctor.objects.count(),  # type: ignore
            'blogs_count': BlogPost.objects.count(),  # type: ignore
        }
        return JsonResponse({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_home_content(request: HttpRequest) -> JsonResponse:
    """
    Real-time content for the home page (top treatments, hospitals, doctors)
    """
    try:
        # Get top treatments
        top_treatments = list(Treatment.objects.all()[:6].values('id', 'name', 'slug'))  # type: ignore
        
        # Get top hospitals
        top_hospitals = list(Hospital.objects.all()[:4].values('id', 'name', 'slug', 'profile_picture', 'is_takeopinion_choice'))  # type: ignore
        
        # Get top doctors
        top_doctors = list(Doctor.objects.all()[:4].values('id', 'name', 'slug', 'profile_picture', 'key_points'))  # type: ignore
        
        # Get latest blogs
        latest_blogs = list(BlogPost.objects.all()[:3].values('id', 'title', 'slug', 'published_at'))  # type: ignore
        
        return JsonResponse({
            'success': True,
            'top_treatments': top_treatments,
            'top_hospitals': top_hospitals,
            'top_doctors': top_doctors,
            'latest_blogs': latest_blogs
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


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