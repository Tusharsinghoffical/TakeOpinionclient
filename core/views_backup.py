from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import Q
from treatments.models import Treatment, TreatmentCategory
from hospitals.models import Hospital
from bookings.models import Booking
from doctors.models import Doctor
import json


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
    }
    
    return render(request, "core/home.html", context)


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "core/contact.html")


def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "core/privacy.html")


def terms(request: HttpRequest) -> HttpResponse:
    return render(request, "core/terms.html")


def health_check(request: HttpRequest) -> HttpResponse:
    return HttpResponse(b"OK")


def static_files_check(request: HttpRequest) -> HttpResponse:
    return render(request, "core/static_check.html")


def search(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q', '')
    results = {}
    
    if query:
        # Search treatments
        treatment_results = Treatment._default_manager.filter(  # type: ignore
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
        # Search hospitals
        hospital_results = Hospital._default_manager.filter(  # type: ignore
            Q(name__icontains=query) | Q(city__icontains=query) | Q(state__name__icontains=query)
        )
        
        # Search doctors
        doctor_results = Doctor._default_manager.filter(  # type: ignore
            Q(name__icontains=query) | Q(specialization__icontains=query)
        )
        
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
                room_options = [
                    {
                        'id': 1,
                        'name': 'Standard Room',
                        'price_per_night': float(hospital.starting_price * 0.1),  # 10% of treatment price
                    },
                    {
                        'id': 2,
                        'name': 'Deluxe Room',
                        'price_per_night': float(hospital.starting_price * 0.15),  # 15% of treatment price
                    },
                    {
                        'id': 3,
                        'name': 'Suite',
                        'price_per_night': float(hospital.starting_price * 0.25),  # 25% of treatment price
                    }
                ]
            
            hospitals_data.append({
                'id': hospital.id,
                'name': hospital.name,
                'city': hospital.city,
                'state': hospital.state.name if hospital.state else '',
                'country': hospital.country.name if hospital.country else '',
                'rating': float(hospital.rating) if hospital.rating else 0,
                'price': float(hospital.starting_price),
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
                'description': treatment.description,
                'starting_price': float(treatment.starting_price),
            }
        })
    except Treatment.DoesNotExist:  # type: ignore
        return JsonResponse({
            'success': False,
            'error': 'Treatment not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while fetching hospitals'
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


 
 
 #   P o r t f o l i o   v i e w   f o r   f r e e l a n c e   s e r v i c e s 
 d e f   p o r t f o l i o ( r e q u e s t :   H t t p R e q u e s t )   - >   H t t p R e s p o n s e : 
         \ 
 
 \ \ D i s p l a y 
 
 t h e 
 
 p o r t f o l i o 
 
 p a g e 
 
 s h o w c a s i n g 
 
 f r e e l a n c e 
 
 s e r v i c e s \ \ \ 
         r e t u r n   r e n d e r ( r e q u e s t ,   \ c o r e / p o r t f o l i o . h t m l \ ) 
 
 