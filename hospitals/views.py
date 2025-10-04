from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Hospital
from feedbacks.models import Feedback  # Add this import


def hospitals_list(request: HttpRequest) -> HttpResponse:
    hospitals = Hospital.objects.all()  # type: ignore
    
    # Get filter parameters from request
    search = request.GET.get('search', '')
    treatment = request.GET.get('treatment', '')
    accreditation = request.GET.get('accreditation', '')
    rating = request.GET.get('rating', '')
    doctor_id = request.GET.get('doctor', '')  # Add doctor filter for related hospitals
    treatment_id = request.GET.get('treatment_id', '')  # Add treatment filter for related hospitals
    
    # Apply search filter
    if search:
        name_filter = Q(name__icontains=search)
        city_filter = Q(city__icontains=search)
        state_filter = Q(state__name__icontains=search)
        hospitals = hospitals.filter(name_filter | city_filter | state_filter)  # type: ignore
    
    # Apply treatment filter
    if treatment:
        hospitals = hospitals.filter(treatments__name__icontains=treatment)  # type: ignore
    
    # Apply accreditation filter
    if accreditation:
        if accreditation == 'JCI':
            hospitals = hospitals.filter(jci_accredited=True)  # type: ignore
        elif accreditation == 'NABH':
            hospitals = hospitals.filter(nabh_accredited=True)  # type: ignore
        elif accreditation == 'ISO':
            hospitals = hospitals.filter(iso_certified=True)  # type: ignore
    
    # Apply rating filter
    if rating:
        if rating == '4.5':
            hospitals = hospitals.filter(rating__gte=4.5)  # type: ignore
        elif rating == '4.0':
            hospitals = hospitals.filter(rating__gte=4.0)  # type: ignore
        elif rating == '3.5':
            hospitals = hospitals.filter(rating__gte=3.5)  # type: ignore
    
    # Add doctor filter for related hospitals
    if doctor_id:
        hospitals = hospitals.filter(doctors__id=doctor_id)  # type: ignore
    
    # Add treatment ID filter for related hospitals
    if treatment_id:
        hospitals = hospitals.filter(treatments__id=treatment_id)  # type: ignore
    
    # Remove duplicates if any filters were applied
    if search or treatment or accreditation or rating or doctor_id or treatment_id:
        hospitals = hospitals.distinct()  # type: ignore
    
    context = {
        'hospitals': hospitals,
        'search_filter': search,
        'treatment_filter': treatment,
        'accreditation_filter': accreditation,
        'rating_filter': rating,
        'doctor_filter': doctor_id,
        'treatment_id_filter': treatment_id,
    }
    
    return render(request, "hospitals/list.html", context)


def hospital_detail(request: HttpRequest, slug: str) -> HttpResponse:
    hospital = get_object_or_404(Hospital, slug=slug)
    # Fetch approved feedback for this hospital
    feedbacks = Feedback.objects.filter(hospital=hospital, is_approved=True).select_related('patient').order_by('-created_at')  # type: ignore
    
    # Paginate treatments
    treatments = hospital.treatments.all().order_by('name')
    treatments_paginator = Paginator(treatments, 10)
    treatments_page_number = request.GET.get('treatments_page')
    treatments_page_obj = treatments_paginator.get_page(treatments_page_number)
    
    # Paginate doctors
    doctors = hospital.doctors.all().order_by('name')
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