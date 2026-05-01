from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from .models import Hospital
from feedbacks.models import Feedback  # Add this import
from treatments.models import Treatment
from doctors.models import Doctor


def hospitals_list(request: HttpRequest) -> HttpResponse:
    hospitals = Hospital.objects.all()  # type: ignore
    
    # Get filter parameters from request
    search = request.GET.get('search', '')
    treatment = request.GET.get('treatment', '')
    accreditation = request.GET.get('accreditation', '')
    rating = request.GET.get('rating', '')
    doctor_id = request.GET.get('doctor', '')  # Add doctor filter for related hospitals
    treatment_id = request.GET.get('treatment_id', '')  # Add treatment filter for related hospitals
    
    # Handle treatment parameter passed from treatment detail page
    if not treatment_id and request.GET.get('treatment'):
        treatment_id = request.GET.get('treatment')
    
    # Apply search filter
    if search:
        name_filter = Q(name__icontains=search)
        city_filter = Q(city__icontains=search)
        state_filter = Q(state__name__icontains=search)
        country_filter = Q(country__name__icontains=search)
        hospitals = hospitals.filter(name_filter | city_filter | state_filter | country_filter)  # type: ignore
    
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
        try:
            rating_value = float(str(rating))
            hospitals = hospitals.filter(rating__gte=rating_value)  # type: ignore
        except (ValueError, TypeError):
            pass
    
    # Add doctor filter for related hospitals
    if doctor_id:
        try:
            doctor_id_int = int(str(doctor_id))
            hospitals = hospitals.filter(doctors__id=doctor_id_int)  # type: ignore
        except (ValueError, TypeError):
            pass
    
    # Add treatment ID filter for related hospitals
    if treatment_id:
        try:
            treatment_id_int = int(str(treatment_id))
            hospitals = hospitals.filter(treatments__id=treatment_id_int)  # type: ignore
        except (ValueError, TypeError):
            pass
    
    # Remove duplicates if any filters were applied
    if search or treatment or accreditation or rating or doctor_id or treatment_id:
        hospitals = hospitals.distinct()  # type: ignore
    
    # Add ordering by rating (top hospitals first)
    hospitals = hospitals.order_by('-rating')  # type: ignore
    
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


@require_http_methods(["GET"])
def search_hospitals_api(request: HttpRequest) -> JsonResponse:
    """
    API endpoint to search for hospitals by name
    """
    query = request.GET.get('query', '')
    
    if not query or len(query) < 2:
        return JsonResponse({
            'success': False,
            'error': 'Query too short'
        })
    
    hospitals = Hospital.objects.filter(name__icontains=query)[:10]  # type: ignore
    
    results = []
    for hospital in hospitals:
        results.append({
            'id': hospital.id,
            'name': hospital.name,
            'slug': hospital.slug,
            'location': f'{hospital.city}, {hospital.state.name if hospital.state else ""}',
            'price': float(hospital.starting_price),
            'url': f'/hospitals/{hospital.slug}/'
        })
    
    return JsonResponse({
        'success': True,
        'results': results
    })