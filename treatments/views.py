from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import TreatmentCategory, Treatment
from hospitals.models import Hospital
from doctors.models import Doctor
from feedbacks.models import Feedback  # Add this import
import json
from typing import Optional


def treatments_home(request: HttpRequest, category_slug: Optional[str] = None) -> HttpResponse:
    # Get all categories
    categories = TreatmentCategory.objects.all().order_by("type", "name")  # type: ignore
    
    # Get filter parameters from request
    search = request.GET.get('search', '')
    hospital = request.GET.get('hospital', '')
    doctor = request.GET.get('doctor', '')
    hospital_id = request.GET.get('hospital_id', '')  # Add hospital filter for related treatments
    doctor_id = request.GET.get('doctor_id', '')  # Add doctor filter for related treatments
    
    # Filter by category if slug is provided
    if category_slug:
        category = get_object_or_404(TreatmentCategory, slug=category_slug)
        treatments = Treatment.objects.filter(category=category).select_related('category')  # type: ignore
    else:
        treatments = Treatment.objects.select_related('category').all()  # type: ignore
    
    # Apply search filter
    if search:
        treatments = treatments.filter(name__icontains=search)  # type: ignore
    
    # Apply hospital filter
    if hospital:
        treatments = treatments.filter(hospitals__name__icontains=hospital)  # type: ignore
    
    # Apply doctor filter
    if doctor:
        treatments = treatments.filter(doctors__name__icontains=doctor)  # type: ignore
    
    # Apply hospital ID filter for related treatments
    if hospital_id:
        treatments = treatments.filter(hospitals__id=hospital_id)  # type: ignore
    
    # Apply doctor ID filter for related treatments
    if doctor_id:
        treatments = treatments.filter(doctors__id=doctor_id)  # type: ignore
    
    # Remove duplicates if any filters were applied
    if search or hospital or doctor or hospital_id or doctor_id:
        treatments = treatments.distinct()  # type: ignore
    
    return render(request, "treatments/home.html", {
        "categories": categories,
        "treatments": treatments,
        "selected_category": category_slug,
        "search_filter": search,
        "hospital_filter": hospital,
        "doctor_filter": doctor,
        "hospital_id_filter": hospital_id,
        "doctor_id_filter": doctor_id,
    })


def treatments_pricing(request: HttpRequest) -> HttpResponse:
    # Get all treatments with their pricing information
    treatments = Treatment.objects.select_related('category').all().order_by('category__type', 'category__name', 'name')  # type: ignore
    
    # Group treatments by category for display
    categories = TreatmentCategory.objects.prefetch_related('treatments').all().order_by("type", "name")  # type: ignore
    
    return render(request, "treatments/pricing.html", {
        "treatments": treatments,
        "categories": categories
    })


def new_treatments_pricing(request: HttpRequest) -> HttpResponse:
    """New pricing page with treatment selection and hospital filtering"""
    # Get all treatment categories for the dropdown
    categories = TreatmentCategory.objects.prefetch_related('treatments').all().order_by("type", "name")  # type: ignore
    
    return render(request, "treatments/new_pricing.html", {
        "categories": categories
    })


def treatment_detail(request: HttpRequest, slug: str) -> HttpResponse:
    treatment = get_object_or_404(Treatment, slug=slug)
    faqs = treatment.faqs.all()
    # Fetch approved feedback for this treatment
    feedbacks = Feedback.objects.filter(treatment=treatment, is_approved=True).select_related('patient').order_by('-created_at')  # type: ignore
    
    # Paginate hospitals
    hospitals = treatment.hospitals.all().order_by('name')
    hospitals_paginator = Paginator(hospitals, 10)
    hospitals_page_number = request.GET.get('hospitals_page')
    hospitals_page_obj = hospitals_paginator.get_page(hospitals_page_number)
    
    # Paginate doctors
    doctors = treatment.doctors.all().order_by('name')
    doctors_paginator = Paginator(doctors, 10)
    doctors_page_number = request.GET.get('doctors_page')
    doctors_page_obj = doctors_paginator.get_page(doctors_page_number)
    
    # Paginate feedbacks (patient reviews)
    feedbacks_paginator = Paginator(feedbacks, 10)
    feedbacks_page_number = request.GET.get('feedbacks_page')
    feedbacks_page_obj = feedbacks_paginator.get_page(feedbacks_page_number)
    
    return render(
        request,
        "treatments/detail.html",
        {
            "treatment": treatment, 
            "hospitals_page_obj": hospitals_page_obj,
            "doctors_page_obj": doctors_page_obj, 
            "faqs": faqs, 
            "feedbacks_page_obj": feedbacks_page_obj
        },
    )


@require_http_methods(["GET"])
def filter_treatments(request: HttpRequest) -> JsonResponse:
    """
    Real-time filtering of treatments based on category and search query
    """
    category_type = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '')
    hospital_query = request.GET.get('hospital', '')
    doctor_query = request.GET.get('doctor', '')
    
    # Get all categories
    categories = TreatmentCategory.objects.all().order_by("type", "name")  # type: ignore
    
    # Filter by category type if not 'all'
    if category_type != 'all':
        categories = categories.filter(type=category_type)
    
    # Prepare data for JSON response
    categories_data = []
    for category in categories:
        treatments = category.treatments.all().order_by('name')
        
        # Filter treatments by search query if provided
        if search_query:
            treatments = treatments.filter(name__icontains=search_query)
        
        # Filter treatments by hospital if provided
        if hospital_query:
            treatments = treatments.filter(hospitals__name__icontains=hospital_query)
        
        # Filter treatments by doctor if provided
        if doctor_query:
            treatments = treatments.filter(doctors__name__icontains=doctor_query)
        
        # Remove duplicates if any filters were applied
        if search_query or hospital_query or doctor_query:
            treatments = treatments.distinct()
        
        treatments_data = [
            {
                'id': treatment.id,
                'name': treatment.name,
                'slug': treatment.slug,
            }
            for treatment in treatments
        ]
        
        categories_data.append({
            'id': category.id,
            'name': category.name,
            'type': category.type,
            'type_display': category.get_type_display(),
            'treatments': treatments_data
        })
    
    return JsonResponse({
        'success': True,
        'categories': categories_data
    })


@require_http_methods(["GET"])
def get_hospitals_for_treatment(request: HttpRequest, treatment_id: int) -> JsonResponse:
    """
    Get hospitals that offer a specific treatment
    """
    try:
        treatment = Treatment.objects.select_related('category').get(id=treatment_id)  # type: ignore
        hospitals = Hospital.objects.filter(treatments=treatment).all().order_by('-rating', 'name')  # type: ignore
        
        hospitals_data = []
        for hospital in hospitals:
            hospitals_data.append({
                'id': hospital.id,
                'name': hospital.name,
                'city': hospital.city,
                'state': hospital.state.name if hospital.state else "",
                'country': hospital.country.name if hospital.country else "",
                'rating': float(hospital.rating),
                'price': float(hospital.starting_price),
                'jci_accredited': hospital.jci_accredited,
                'nabh_accredited': hospital.nabh_accredited,
                'iso_certified': hospital.iso_certified,
                'is_takeopinion_choice': hospital.is_takeopinion_choice,
                'profile_picture': hospital.profile_picture,
                'slug': hospital.slug
            })
        
        return JsonResponse({
            'success': True,
            'treatment': {
                'id': treatment.id,
                'name': treatment.name,
                'slug': treatment.slug,
                'category': treatment.category.name,
                'starting_price': float(treatment.starting_price),
            },
            'hospitals': hospitals_data
        })
    except Treatment.DoesNotExist:  # type: ignore
        return JsonResponse({
            'success': False,
            'error': 'Treatment not found'
        }, status=404)


@require_http_methods(["GET"])
def search_entities(request: HttpRequest) -> JsonResponse:
    """
    Search for treatments, doctors, or hospitals by name
    """
    entity_type = request.GET.get('type', '')
    query = request.GET.get('query', '')

    if not query or len(query) < 2:
        return JsonResponse({
            'success': False,
            'error': 'Query too short'
        })

    results = []

    if entity_type == 'treatment':
        treatments = Treatment.objects.filter(name__icontains=query)[:10]  # type: ignore
        for treatment in treatments:
            results.append({
                'id': treatment.id,
                'name': treatment.name,
                'slug': treatment.slug,
                'price': float(treatment.starting_price),
                'category': treatment.category.name if treatment.category else '',
                'url': f'/treatments/{treatment.slug}/'
            })

    elif entity_type == 'doctor':
        doctors = Doctor.objects.filter(name__icontains=query)[:10]  # type: ignore
        for doctor in doctors:
            # Use a default price since doctors don't have a direct price field
            # We'll use the average of treatments they offer or a default value
            default_price = 100.0  # Default consultation fee
            results.append({
                'id': doctor.id,
                'name': doctor.name,
                'slug': doctor.slug,
                'specialty': doctor.specialization if doctor.specialization else '',
                'price': default_price,
                'url': f'/doctors/{doctor.slug}/'
            })

    elif entity_type == 'hospital':
        hospitals = Hospital.objects.filter(name__icontains=query)[:10]  # type: ignore
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


def treatment_comparison(request: HttpRequest, slug: str) -> HttpResponse:
    """Display comparison of the same treatment across different hospitals"""
    treatment = get_object_or_404(Treatment, slug=slug)
    
    # Get all hospitals that offer this treatment
    hospitals = treatment.hospitals.all().prefetch_related('doctors')
    
    # Get all doctors who offer this treatment
    doctors = treatment.doctors.all().prefetch_related('hospitals')
    
    # Create comparison data
    comparison_data = []
    for hospital in hospitals:
        # Get doctors at this hospital who offer this treatment
        hospital_doctors = doctors.filter(hospitals=hospital)
        
        comparison_data.append({
            'hospital': hospital,
            'doctors': hospital_doctors,
            'price': hospital.starting_price,
        })
    
    context = {
        'treatment': treatment,
        'comparison_data': comparison_data,
    }
    return render(request, 'treatments/comparison.html', context)
