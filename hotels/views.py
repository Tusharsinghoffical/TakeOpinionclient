from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Hotel, HotelImage
from hospitals.models import Hospital
from bookings.models import Booking
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)


def hotels_list(request: HttpRequest) -> HttpResponse:
    """Display list of hotels with filtering options"""
    hotels = Hotel._default_manager.filter(is_active=True)
    
    # Get filter parameters
    city = request.GET.get('city', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    rating = request.GET.get('rating', '')
    
    # Apply filters
    if city:
        hotels = hotels.filter(Q(city__icontains=city) | Q(state__icontains=city))
    
    if min_price:
        hotels = hotels.filter(price_per_night__gte=min_price)
    
    if max_price:
        hotels = hotels.filter(price_per_night__lte=max_price)
    
    if rating:
        hotels = hotels.filter(rating__gte=rating)
    
    # Sort by rating by default
    hotels = hotels.order_by('-rating')
    
    context = {
        'hotels': hotels,
        'city_filter': city,
        'min_price_filter': min_price,
        'max_price_filter': max_price,
        'rating_filter': rating,
    }
    
    return render(request, 'hotels/list.html', context)


def hotel_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Display detailed information about a specific hotel"""
    hotel = get_object_or_404(Hotel, slug=slug, is_active=True)
    images = hotel.images.all()
    nearby_hospitals = hotel.nearby_hospitals.all()
    
    context = {
        'hotel': hotel,
        'images': images,
        'nearby_hospitals': nearby_hospitals,
    }
    
    return render(request, 'hotels/detail.html', context)


@login_required
def suggest_hotels_after_payment(request: HttpRequest, booking_id: int) -> HttpResponse:
    """Suggest hotels after a successful payment"""
    # Get the booking
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Get the hospital associated with the booking
    hospital = booking.preferred_hospital
    
    # Get nearby hotels
    if hospital:
        hotels = Hotel._default_manager.filter(nearby_hospitals=hospital, is_active=True).order_by('-rating')[:5]
    else:
        # If no hospital, get hotels in the same city as the patient's preferred location
        hotels = Hotel._default_manager.filter(is_active=True).order_by('-rating')[:5]
    
    context = {
        'booking': booking,
        'hotels': hotels,
        'hospital': hospital,
    }
    
    return render(request, 'hotels/suggestions.html', context)


@require_http_methods(["GET"])
def search_hotels_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for searching hotels"""
    query = request.GET.get('q', '')
    city = request.GET.get('city', '')
    
    hotels = Hotel._default_manager.filter(is_active=True)
    
    if query:
        # Search in name, description, and amenities
        name_results = hotels.filter(name__icontains=query)
        description_results = hotels.filter(description__icontains=query)
        amenities_results = hotels.filter(amenities__icontains=query)
        # Combine results using union
        hotels = name_results.union(description_results, amenities_results)
    
    if city:
        hotels = hotels.filter(city__icontains=city)
    
    # Limit to 10 results
    hotels = hotels[:10]
    
    # Prepare data for JSON response
    hotel_data = []
    for hotel in hotels:
        hotel_data.append({
            'id': hotel.id,
            'name': hotel.name,
            'address': hotel.address,
            'city': hotel.city,
            'rating': float(hotel.rating),
            'price_per_night': float(hotel.price_per_night),
            'image_url': hotel.images.first().image.url if hotel.images.first() else '',
        })
    
    return JsonResponse({
        'hotels': hotel_data,
        'count': len(hotel_data)
    })