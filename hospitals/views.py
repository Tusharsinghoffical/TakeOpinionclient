from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Hospital
from feedbacks.models import Feedback  # Add this import


def hospitals_list(request: HttpRequest) -> HttpResponse:
    hospitals = Hospital._default_manager.all()  # type: ignore
    
    # Get filter parameters from request
    search = request.GET.get('search', '')
    treatment = request.GET.get('treatment', '')
    accreditation = request.GET.get('accreditation', '')
    rating = request.GET.get('rating', '')
    
    # Apply search filter
    if search:
        search_filter = Q(name__icontains=search) | Q(city__icontains=search) | Q(state__name__icontains=search)  # type: ignore
        hospitals = hospitals.filter(search_filter)  # type: ignore
    
    # Apply filters if provided
    if treatment:
        hospitals = hospitals.filter(treatments__name=treatment)  # type: ignore
    
    if accreditation:
        if accreditation == 'JCI':
            hospitals = hospitals.filter(jci_accredited=True)  # type: ignore
        elif accreditation == 'NABH':
            hospitals = hospitals.filter(nabh_accredited=True)  # type: ignore
        elif accreditation == 'ISO':
            hospitals = hospitals.filter(iso_certified=True)  # type: ignore
    
    if rating:
        try:
            rating_value = float(str(rating))
            hospitals = hospitals.filter(rating__gte=rating_value)  # type: ignore
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
    # Fetch approved feedback for this hospital
    feedbacks = Feedback.objects.filter(hospital=hospital, is_approved=True).select_related('patient')  # type: ignore
    
    # Paginate treatments
    treatments = hospital.treatments.all()
    treatments_paginator = Paginator(treatments, 10)
    treatments_page_number = request.GET.get('treatments_page')
    treatments_page_obj = treatments_paginator.get_page(treatments_page_number)
    
    # Paginate doctors
    doctors = hospital.doctors.all()
    doctors_paginator = Paginator(doctors, 10)
    doctors_page_number = request.GET.get('doctors_page')
    doctors_page_obj = doctors_paginator.get_page(doctors_page_number)
    
    # Paginate feedbacks (patient reviews)
    feedbacks_paginator = Paginator(feedbacks, 10)
    feedbacks_page_number = request.GET.get('feedbacks_page')
    feedbacks_page_obj = feedbacks_paginator.get_page(feedbacks_page_number)
    
    return render(request, "hospitals/detail.html", {
        "hospital": hospital, 
        "treatments_page_obj": treatments_page_obj,
        "doctors_page_obj": doctors_page_obj,
        "feedbacks_page_obj": feedbacks_page_obj
    })


def hospital_test(request: HttpRequest, slug: str) -> HttpResponse:
    hospital = get_object_or_404(Hospital, slug=slug)
    return render(request, "hospitals/test.html", {"hospital": hospital})


def hospital_simple_test(request: HttpRequest, slug: str) -> HttpResponse:
    hospital = get_object_or_404(Hospital, slug=slug)
    return render(request, "hospitals/simple_test.html", {"hospital": hospital})


def hospital_media_debug(request: HttpRequest, slug: str) -> HttpResponse:
    hospital = get_object_or_404(Hospital, slug=slug)
    media_items = hospital.media_items.all()  # type: ignore
    
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