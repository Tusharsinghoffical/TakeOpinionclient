from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import TreatmentCategory, Treatment
from hospitals.models import Hospital
from feedbacks.models import Feedback  # Add this import
import json
from typing import Optional


def treatments_home(request: HttpRequest, category_slug: Optional[str] = None) -> HttpResponse:
    # Get all categories
    categories = TreatmentCategory.objects.all().order_by("type", "name")  # type: ignore
    
    # Filter by category if slug is provided
    if category_slug:
        category = get_object_or_404(TreatmentCategory, slug=category_slug)
        treatments = Treatment.objects.filter(category=category).select_related('category')  # type: ignore
    else:
        treatments = Treatment.objects.select_related('category').all()  # type: ignore
    
    return render(request, "treatments/home.html", {
        "categories": categories,
        "treatments": treatments,
        "selected_category": category_slug
    })


def treatments_pricing(request: HttpRequest) -> HttpResponse:
    # Get all treatments with their pricing information
    treatments = Treatment.objects.select_related('category').all()  # type: ignore
    
    # Group treatments by category for display
    categories = TreatmentCategory.objects.prefetch_related('treatments').all()  # type: ignore
    
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
    feedbacks = Feedback.objects.filter(treatment=treatment, is_approved=True).select_related('patient')  # type: ignore
    
    # Paginate hospitals
    hospitals = treatment.hospitals.all()
    hospitals_paginator = Paginator(hospitals, 10)
    hospitals_page_number = request.GET.get('hospitals_page')
    hospitals_page_obj = hospitals_paginator.get_page(hospitals_page_number)
    
    # Paginate doctors
    doctors = treatment.doctors.all()
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
    
    # Get all categories
    categories = TreatmentCategory.objects.all().order_by("type", "name")  # type: ignore
    
    # Filter by category type if not 'all'
    if category_type != 'all':
        categories = categories.filter(type=category_type)
    
    # Prepare data for JSON response
    categories_data = []
    for category in categories:
        treatments = category.treatments.all()
        
        # Filter treatments by search query if provided
        if search_query:
            treatments = treatments.filter(name__icontains=search_query)
        
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
        hospitals = Hospital.objects.filter(treatments=treatment).all()  # type: ignore
        
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