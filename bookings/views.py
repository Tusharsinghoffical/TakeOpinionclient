from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Booking, Accommodation
from treatments.models import Treatment, TreatmentCategory
from doctors.models import Doctor
from hospitals.models import Hospital
from accounts.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
import logging

# Set up logging
logger = logging.getLogger(__name__)

def booking_page(request: HttpRequest) -> HttpResponse:
    # Get all treatments, doctors, and hospitals for the dropdowns
    treatments = Treatment.objects.all().order_by('name')  # type: ignore
    doctors = Doctor.objects.all().order_by('name')  # type: ignore
    hospitals = Hospital.objects.all().order_by('name')  # type: ignore
    
    context = {
        'treatments': treatments,
        'doctors': doctors,
        'hospitals': hospitals
    }
    
    if request.method == 'POST':
        # Process the booking form submission
        try:
            # Get form data
            treatment_id = request.POST.get('treatment')
            special_requirements = request.POST.get('special_requirements')
            preferred_doctor_id = request.POST.get('preferred_doctor')
            preferred_hospital_id = request.POST.get('preferred_hospital')
            preferred_date = request.POST.get('preferred_date')
            budget = request.POST.get('budget')
            medical_history = request.POST.get('medical_history')
            travel_companions = request.POST.get('travel_companions')
            urgency = request.POST.get('urgency')
            agree_terms = request.POST.get('agree_terms')
            
            # Validate required fields
            if not treatment_id:
                messages.error(request, 'Please select a treatment type.')
                return render(request, "bookings/booking.html", context)
            
            if not agree_terms:
                messages.error(request, 'You must agree to the Terms of Service and Privacy Policy.')
                return render(request, "bookings/booking.html", context)
            
            # Get the treatment object
            treatment = get_object_or_404(Treatment, id=treatment_id)
            
            # Get preferred doctor and hospital if provided
            preferred_doctor = None
            preferred_hospital = None
            
            if preferred_doctor_id:
                preferred_doctor = get_object_or_404(Doctor, id=preferred_doctor_id)
            
            if preferred_hospital_id:
                preferred_hospital = get_object_or_404(Hospital, id=preferred_hospital_id)
            
            # Create a booking record in the database
            # Get or create user profile
            user_profile = None
            if hasattr(request, 'user') and request.user.is_authenticated:  # type: ignore
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)  # type: ignore
            
            # Create booking
            booking = Booking(
                treatment=treatment,
                preferred_doctor=preferred_doctor,
                preferred_hospital=preferred_hospital,
                patient=user_profile,
                preferred_date=preferred_date if preferred_date else None,
                status='pending'
            )
            
            # Set amount
            if budget:
                booking.amount = Decimal(str(budget))  # type: ignore
            else:
                booking.amount = treatment.starting_price  # type: ignore
            
            booking.save()  # type: ignore
            
            # Send confirmation (in a real implementation, you would send an email)
            messages.success(request, f'Your booking request for {treatment.name} has been submitted successfully! Our team will contact you within 24 hours to confirm details. Booking ID: {booking.id}')  # type: ignore
            
            # Redirect to prevent form resubmission
            return redirect('booking_confirmation', booking_id=booking.id)  # type: ignore
            
        except Exception as e:
            logger.error(f"Error processing booking: {str(e)}", exc_info=True)
            messages.error(request, 'An error occurred while processing your booking request. Please try again.')
    
    return render(request, "bookings/booking.html", context)


def booking_confirmation(request: HttpRequest, booking_id: int) -> HttpResponse:
    """Display booking confirmation page"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Get accommodations near the booked hospital or doctor's hospital
    accommodations = []
    if booking.preferred_hospital:
        # Get accommodations for the preferred hospital
        accommodations = Accommodation.objects.filter(hospital=booking.preferred_hospital)[:4]  # type: ignore
    elif booking.preferred_doctor and booking.preferred_doctor.hospitals.exists():  # type: ignore
        # Get accommodations for the first hospital of the preferred doctor
        first_hospital = booking.preferred_doctor.hospitals.first()  # type: ignore
        if first_hospital:
            accommodations = Accommodation.objects.filter(hospital=first_hospital)[:4]  # type: ignore
    
    context = {
        'booking': booking,
        'accommodations': accommodations
    }
    
    return render(request, "bookings/confirmation.html", context)


def post_payment(request: HttpRequest) -> HttpResponse:
    return render(request, "bookings/post_payment.html")


@login_required
def consultation_booking(request, doctor_id):
    """Handle consultation booking with Google Meet integration"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        # Get form data
        consultation_type = request.POST.get('consultation_type')
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time')
        treatment_id = request.POST.get('treatment_id')
        
        # Validate data
        if not all([consultation_type, preferred_date, preferred_time]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'bookings/consultation_booking.html', {
                'doctor': doctor,
                'treatments': doctor.treatments.all()
            })
        
        try:
            # Create a booking record
            treatment = None
            if treatment_id:
                try:
                    # Use get_object_or_404 to handle the Treatment object retrieval
                    treatment = get_object_or_404(Treatment, id=treatment_id)
                except Exception as e:
                    logger.error(f"Treatment with id {treatment_id} does not exist: {str(e)}")
                    pass
            
            # For consultation, we'll use a placeholder treatment if none selected
            if not treatment:
                # Get or create a general consultation treatment
                category, created = TreatmentCategory.objects.get_or_create(
                    name="General",
                    defaults={'type': 'medical'}
                )  # type: ignore
                treatment, created = Treatment.objects.get_or_create(
                    name="General Consultation",
                    defaults={
                        'description': "General medical consultation",
                        'category': category,
                        'starting_price': 50.00
                    }
                )  # type: ignore
            
            # Create booking
            booking = Booking(
                treatment=treatment,
                preferred_doctor=doctor,
                patient=request.user.userprofile,  # type: ignore
                preferred_date=preferred_date,
                status='pending'
            )  # type: ignore
            
            # Set amount
            if treatment:
                booking.amount = treatment.starting_price  # type: ignore
            else:
                booking.amount = Decimal('50.00')  # type: ignore
            
            booking.save()  # type: ignore
            
            # Generate Google Meet link (in a real implementation, this would use Google Calendar API)
            meet_link = f"https://meet.google.com/{uuid.uuid4().hex[:3]}-{uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:3]}"
            
            # Store consultation details
            consultation_details = {
                'type': consultation_type,
                'meet_link': meet_link,
                'date': preferred_date,
                'time': preferred_time,
                'booking_id': booking.id,  # type: ignore
                'amount': float(treatment.starting_price) if treatment else 50.00
            }
            
            # In a real implementation, you would:
            # 1. Use Google Calendar API to create the meeting
            # 2. Send email invitations to both parties
            # 3. Store the meeting details in the database
            
            messages.success(request, f'Consultation booked successfully! Your {consultation_type} consultation is scheduled for {preferred_date} at {preferred_time}.')
            return render(request, 'bookings/consultation_confirmation.html', {
                'doctor': doctor,
                'consultation_details': consultation_details,
                'meet_link': meet_link
            })
            
        except Exception as e:
            logger.error(f"Error booking consultation: {str(e)}", exc_info=True)
            messages.error(request, 'An error occurred while booking your consultation. Please try again.')
            return render(request, 'bookings/consultation_booking.html', {
                'doctor': doctor,
                'treatments': doctor.treatments.all()
            })
    
    # GET request - show booking form
    return render(request, 'bookings/consultation_booking.html', {
        'doctor': doctor,
        'treatments': doctor.treatments.all()
    })


@csrf_exempt
def create_google_meet(request):
    """API endpoint to simulate Google Meet creation"""
    if request.method == 'POST':
        # In a real implementation, this would use Google Calendar API
        # For now, we'll generate a mock Meet link
        meet_link = f"https://meet.google.com/{uuid.uuid4().hex[:3]}-{uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:3]}"
        
        return JsonResponse({
            'success': True,
            'meet_link': meet_link,
            'message': 'Google Meet link created successfully'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})