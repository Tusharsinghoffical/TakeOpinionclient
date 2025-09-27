from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from .models import Hospital


def hospitals_list(request: HttpRequest) -> HttpResponse:
    hospitals = Hospital.objects.all()
    
    # Get filter parameters from request
    search = request.GET.get('search', '')
    treatment = request.GET.get('treatment', '')
    accreditation = request.GET.get('accreditation', '')
    rating = request.GET.get('rating', '')
    
    # Apply search filter
    if search:
        hospitals = hospitals.filter(
            Q(name__icontains=search) | Q(city__icontains=search) | Q(state__name__icontains=search)
        )
    
    # Apply filters if provided
    if treatment:
        hospitals = hospitals.filter(treatments__name=treatment)
    
    if accreditation:
        if accreditation == 'JCI':
            hospitals = hospitals.filter(jci_accredited=True)
        elif accreditation == 'NABH':
            hospitals = hospitals.filter(nabh_accredited=True)
        elif accreditation == 'ISO':
            hospitals = hospitals.filter(iso_certified=True)
    
    if rating:
        try:
            rating_value = float(str(rating))
            hospitals = hospitals.filter(rating__gte=rating_value)
        except (ValueError, TypeError):
            pass  # Invalid rating value, ignore filter
    
    context = {
        'hospitals': hospitals,
        'search_filter': search,
        'treatment_filter': treatment,
        'accreditation_filter': accreditation,
        'rating_filter': rating,
    }
    
    return render(request, "hospitals/list.html", context)


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