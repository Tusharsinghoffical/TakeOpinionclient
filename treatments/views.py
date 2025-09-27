from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import TreatmentCategory, Treatment
import json


def treatments_home(request: HttpRequest) -> HttpResponse:
    categories = TreatmentCategory.objects.all().order_by("type", "name")  # type: ignore
    return render(request, "treatments/home.html", {"categories": categories})


def treatments_pricing(request: HttpRequest) -> HttpResponse:
    # Get all treatments with their pricing information
    treatments = Treatment.objects.select_related('category').all()
    
    # Group treatments by category for display
    categories = TreatmentCategory.objects.prefetch_related('treatments').all()
    
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
    hospitals = treatment.hospitals.all()[:5]
    doctors = treatment.doctors.all()[:5]
    faqs = treatment.faqs.all()
    return render(
        request,
        "treatments/detail.html",
        {"treatment": treatment, "hospitals": hospitals, "doctors": doctors, "faqs": faqs},
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