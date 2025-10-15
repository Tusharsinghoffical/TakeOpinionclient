from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from treatments.models import Treatment, TreatmentCategory
from hospitals.models import Hospital
from bookings.models import Booking
from doctors.models import Doctor
import json
import os
import sys


def portfolio(request: HttpRequest) -> HttpResponse:
    """Display the portfolio page showcasing freelance services"""
    return render(request, "core/portfolio.html")


def home(request: HttpRequest) -> HttpResponse:
    # Get featured treatments
    featured_treatments = Treatment.objects.all()[:6]  # type: ignore
    
    # Get featured hospitals
    featured_hospitals = Hospital.objects.all()[:4]  # type: ignore
    
    # Get featured doctors
    featured_doctors = Doctor.objects.all()[:4]  # type: ignore
    
    # Get counts for stats section
    treatments_count = Treatment._default_manager.count()  # type: ignore
    hospitals_count = Hospital._default_manager.count()  # type: ignore
    doctors_count = Doctor._default_manager.count()  # type: ignore
    
    # Get top doctors (highest rated)
    top_doctors = Doctor.objects.order_by('-rating')[:4]  # type: ignore
    
    # Get top hospitals (highest rated)
    top_hospitals = Hospital.objects.order_by('-rating')[:4]  # type: ignore
    
    # Get treatment categories
    treatment_categories = TreatmentCategory.objects.all()[:6]  # type: ignore
    
    # Get top treatments (ordered by review count)
    top_treatments = Treatment.objects.order_by('-review_count')[:6]  # type: ignore
    
    # Get recent feedback (reviews) - both text and video
    from feedbacks.models import Feedback
    recent_feedback = Feedback.objects.filter(is_approved=True).select_related('patient__user').order_by('-created_at')[:6]  # type: ignore
    
    context = {
        'featured_treatments': featured_treatments,
        'featured_hospitals': featured_hospitals,
        'featured_doctors': featured_doctors,
        'treatments_count': treatments_count,
        'hospitals_count': hospitals_count,
        'doctors_count': doctors_count,
        'top_doctors': top_doctors,
        'top_hospitals': top_hospitals,
        'treatment_categories': treatment_categories,
        'top_treatments': top_treatments,
        'recent_feedback': recent_feedback,  # Add recent feedback to context
    }
    
    return render(request, "core/home.html", context)


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "core/contact.html")


def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "core/privacy.html")


def terms(request: HttpRequest) -> HttpResponse:
    return render(request, "core/terms.html")


@csrf_exempt
def health_check(request):
    """
    Health check endpoint for Render deployment
    Returns a JSON response indicating the application status
    """
    try:
        # Check if database is accessible
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "OK"
    except Exception as e:
        db_status = f"ERROR: {str(e)}"
    
    # Get application info
    app_info = {
        "status": "healthy" if db_status == "OK" else "unhealthy",
        "database": db_status,
        "python_version": sys.version,
        "environment": os.environ.get("DJANGO_SETTINGS_MODULE", "Not set"),
        "debug": os.environ.get("DEBUG", "Not set"),
    }
    
    return JsonResponse(app_info)


@cache_page(60 * 5)  # Cache for 5 minutes
def cached_health_check(request):
    """
    Cached health check endpoint for monitoring
    """
    return health_check(request)


def static_files_check(request: HttpRequest) -> HttpResponse:
    return render(request, "core/static_check.html")


def search(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q', '')
    results = {}
    
    if query:
        # Search treatments
        treatment_filter = Q(name__icontains=query) | Q(description__icontains=query)  # type: ignore
        treatment_results = Treatment._default_manager.filter(treatment_filter)  # type: ignore
        
        # Search hospitals
        hospital_filter = Q(name__icontains=query) | Q(city__icontains=query) | Q(state__name__icontains=query)  # type: ignore
        hospital_results = Hospital._default_manager.filter(hospital_filter)  # type: ignore
        
        # Search doctors
        doctor_filter = Q(name__icontains=query) | Q(specialization__icontains=query)  # type: ignore
        doctor_results = Doctor._default_manager.filter(doctor_filter)  # type: ignore
        
        results = {
            'treatments': treatment_results,
            'hospitals': hospital_results,
            'doctors': doctor_results,
        }
    else:
        results = {
            'treatments': Treatment._default_manager.none(),  # type: ignore
            'hospitals': Hospital._default_manager.none(),  # type: ignore
            'doctors': Doctor._default_manager.none(),  # type: ignore
        }
    
    # Calculate total results
    total_results = sum(len(results[key]) for key in results)
    
    context = {
        'query': query,
        'total_results': total_results,
        'doctors': results['doctors'],
        'hospitals': results['hospitals'],
        'treatments': results['treatments'],
        # blog_posts is optional and not currently implemented
    }
    
    return render(request, "core/search_results.html", context)


def get_home_stats(request: HttpRequest) -> JsonResponse:
    # Get stats for home page
    total_treatments = Treatment._default_manager.count()  # type: ignore
    total_hospitals = Hospital._default_manager.count()  # type: ignore
    total_doctors = Doctor._default_manager.count()  # type: ignore
    total_bookings = Booking._default_manager.count()  # type: ignore
    
    stats = {
        'treatments': total_treatments,
        'hospitals': total_hospitals,
        'doctors': total_doctors,
        'bookings': total_bookings,
    }
    
    return JsonResponse(stats)


def get_home_content(request: HttpRequest) -> JsonResponse:
    # Get featured content for home page
    featured_treatments = list(Treatment._default_manager.all()[:3].values('id', 'name', 'slug', 'starting_price'))  # type: ignore
    featured_hospitals = list(Hospital._default_manager.all()[:3].values('id', 'name', 'slug', 'rating'))  # type: ignore
    
    content = {
        'treatments': featured_treatments,
        'hospitals': featured_hospitals,
    }
    
    return JsonResponse(content)


def pricing_page(request: HttpRequest) -> HttpResponse:
    """Display the pricing page with treatment selection and hospital listings"""
    # Get all treatments for the dropdown
    treatments = Treatment._default_manager.all().order_by('name')  # type: ignore
    
    context = {
        'treatments': treatments,
    }
    
    return render(request, "core/pricing.html", context)


def get_hospitals_by_treatment(request: HttpRequest, treatment_id: int) -> JsonResponse:
    """API endpoint to get hospitals by treatment with pricing information"""
    try:
        treatment = Treatment._default_manager.get(id=treatment_id)  # type: ignore
        hospitals = treatment.hospitals.all().order_by('-rating')  # type: ignore
        
        hospitals_data = []
        for hospital in hospitals:
            # Get room options for this hospital
            accommodations = hospital.accommodations.all()[:3]  # type: ignore
            room_options = []
            for accommodation in accommodations:
                room_options.append({
                    'id': accommodation.id,
                    'name': accommodation.name,
                    'price_per_night': float(accommodation.price_per_night),
                })
            
            # If no accommodations found, provide default room options
            if not room_options:
                # Convert Decimal to float properly
                base_price = float(hospital.starting_price) if hospital.starting_price else 5000.0
                room_options = [
                    {
                        'id': 1,
                        'name': 'Standard Room',
                        'price_per_night': base_price * 0.1,  # 10% of treatment price
                    },
                    {
                        'id': 2,
                        'name': 'Deluxe Room',
                        'price_per_night': base_price * 0.15,  # 15% of treatment price
                    },
                    {
                        'id': 3,
                        'name': 'Suite',
                        'price_per_night': base_price * 0.25,  # 25% of treatment price
                    }
                ]
            
            hospitals_data.append({
                'id': hospital.id,
                'name': hospital.name,
                'city': hospital.city or '',
                'state': hospital.state.name if hospital.state else '',
                'country': hospital.country.name if hospital.country else '',
                'rating': float(hospital.rating) if hospital.rating else 0,
                'price': float(hospital.starting_price) if hospital.starting_price else 0,
                'success_rate': 95.0,  # This would come from the model in a real implementation
                'is_takeopinion_choice': hospital.is_takeopinion_choice,
                'jci_accredited': hospital.jci_accredited,
                'nabh_accredited': hospital.nabh_accredited,
                'iso_certified': hospital.iso_certified,
                'room_options': room_options,
            })
        
        return JsonResponse({
            'success': True,
            'hospitals': hospitals_data,
            'treatment': {
                'id': treatment.id,
                'name': treatment.name,
                'description': treatment.description or '',
                'starting_price': float(treatment.starting_price) if treatment.starting_price else 0,
            }
        })
    except Treatment.DoesNotExist:  # type: ignore
        return JsonResponse({
            'success': False,
            'error': 'Treatment not found'
        }, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()  # For debugging
        return JsonResponse({
            'success': False,
            'error': f'An error occurred while fetching hospitals: {str(e)}'
        }, status=500)


def debug_home_stats(request: HttpRequest) -> HttpResponse:
    """Debug view to check if stats are being passed correctly"""
    # Get counts for stats section
    treatments_count = Treatment._default_manager.count()  # type: ignore
    hospitals_count = Hospital._default_manager.count()  # type: ignore
    doctors_count = Doctor._default_manager.count()  # type: ignore
    
    context = {
        'treatments_count': treatments_count,
        'hospitals_count': hospitals_count,
        'doctors_count': doctors_count,
    }
    
    return JsonResponse(context)


def debug_home_page(request: HttpRequest) -> HttpResponse:
    """Debug view to check all data being passed to home template"""
    # Get all the data that's passed to the home view
    featured_treatments = Treatment.objects.all()[:6]  # type: ignore
    featured_hospitals = Hospital.objects.all()[:4]  # type: ignore
    featured_doctors = Doctor.objects.all()[:4]  # type: ignore
    
    treatments_count = Treatment._default_manager.count()  # type: ignore
    hospitals_count = Hospital._default_manager.count()  # type: ignore
    doctors_count = Doctor._default_manager.count()  # type: ignore
    
    top_doctors = Doctor.objects.order_by('-rating')[:4]  # type: ignore
    top_hospitals = Hospital.objects.order_by('-rating')[:4]  # type: ignore
    treatment_categories = TreatmentCategory.objects.all()[:6]  # type: ignore
    top_treatments = Treatment.objects.order_by('-review_count')[:6]  # type: ignore
    
    # Create a debug context with all the data
    debug_context = {
        'featured_treatments_count': featured_treatments.count(),
        'featured_hospitals_count': featured_hospitals.count(),
        'featured_doctors_count': featured_doctors.count(),
        'treatments_count': treatments_count,
        'hospitals_count': hospitals_count,
        'doctors_count': doctors_count,
        'top_doctors_count': top_doctors.count(),
        'top_hospitals_count': top_hospitals.count(),
        'treatment_categories_count': treatment_categories.count(),
        'top_treatments_count': top_treatments.count(),
        'featured_treatments': list(featured_treatments.values('name', 'slug')),
        'featured_hospitals': list(featured_hospitals.values('name', 'slug')),
        'featured_doctors': list(featured_doctors.values('name', 'slug', 'specialization')),
        'top_doctors': list(top_doctors.values('name', 'slug', 'specialization', 'rating')),
        'top_hospitals': list(top_hospitals.values('name', 'slug', 'city', 'rating')),
        'treatment_categories': list(treatment_categories.values('name', 'slug')),
        'top_treatments': list(top_treatments.values('name', 'slug', 'category__name')),
    }
    
    return JsonResponse(debug_context)


def debug_stats_page(request: HttpRequest) -> HttpResponse:
    """Debug page for home stats"""
    return render(request, "core/debug_stats.html")


def test_stats_page(request: HttpRequest) -> HttpResponse:
    """Test page for home stats"""
    return render(request, "core/test_stats.html")