from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Hospital


def hospitals_list(request: HttpRequest) -> HttpResponse:
    hospitals = Hospital.objects.all()
    return render(request, "hospitals/list.html", {"hospitals": hospitals})


def hospital_detail(request: HttpRequest, slug: str) -> HttpResponse:
    hospital = get_object_or_404(Hospital, slug=slug)
    return render(request, "hospitals/detail.html", {"hospital": hospital})


def hospital_test(request: HttpRequest, slug: str) -> HttpResponse:
    hospital = get_object_or_404(Hospital, slug=slug)
    return render(request, "hospitals/test.html", {"hospital": hospital})


def hospital_simple_test(request: HttpRequest, slug: str) -> HttpResponse:
    hospital = get_object_or_404(Hospital, slug=slug)
    return render(request, "hospitals/simple_test.html", {"hospital": hospital})


def hospital_media_debug(request: HttpRequest, slug: str) -> HttpResponse:
    hospital = get_object_or_404(Hospital, slug=slug)
    media_items = hospital.media_items.all()
    
    # Debug information
    debug_info = {
        'hospital_name': hospital.name,
        'media_count': media_items.count(),
        'media_items': []
    }
    
    for media in media_items:
        debug_info['media_items'].append({
            'id': media.id,
            'image_url': media.image_url
        })
    
    return render(request, "hospitals/simple_test.html", {
        "hospital": hospital,
        "debug_info": debug_info
    })