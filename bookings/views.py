from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Booking, Accommodation, MedicalReport
from treatments.models import Treatment, TreatmentCategory
from doctors.models import Doctor
from hospitals.models import Hospital
from accounts.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
import logging

# Set up logging
logger = logging.getLogger(__name__)


def appointment_booking(request: HttpRequest) -> HttpResponse:
    """Display the simple appointment booking page"""
    # Get all doctors for the dropdown
    doctors = Doctor.objects.all().order_by('name')  # type: ignore
    
    if request.method == 'POST':
        # Process the appointment form submission
        try:
            # Get form data
            patient_name = request.POST.get('patient_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')
            department = request.POST.get('department')
            doctor_id = request.POST.get('doctor')
            reason = request.POST.get('reason')
            
            # Validate required fields
            if not all([patient_name, phone, appointment_date, appointment_time, department]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, "bookings/appointment.html", {"doctors": doctors})
            
            # Create a simple booking record
            doctor = None
            if doctor_id:
                try:
                    doctor = Doctor.objects.get(id=doctor_id)  # type: ignore
                except Doctor.DoesNotExist:  # type: ignore
                    pass
            
            # Create booking with minimal information
            booking = Booking(
                treatment=None,  # Not required for simple appointment
                preferred_doctor=doctor,
                preferred_hospital=None,  # Not required for simple appointment
                patient=None,  # Not required for simple appointment
                preferred_date=appointment_date,
                status='pending',
                notes=f"Appointment for {department}. Reason: {reason}" if reason else f"Appointment for {department}",
                amount=0.00
            )
            
            booking.save()  # type: ignore
            
            # Send confirmation message
            messages.success(request, f'Your appointment has been booked successfully for {appointment_date} at {appointment_time}. Our team will contact you shortly to confirm the details. Booking ID: {booking.id}')  # type: ignore
            
        except Exception as e:
            logger.error(f"Error processing appointment: {str(e)}", exc_info=True)
            messages.error(request, 'An error occurred while booking your appointment. Please try again.')
    
    context = {
        'doctors': doctors,
    }
    
    return render(request, "bookings/appointment.html", context)


def new_booking_page(request: HttpRequest) -> HttpResponse:
    """Display the new multi-step booking page"""
    # Get all treatments for the first step
    treatments = Treatment.objects.all().order_by('name')  # type: ignore
    
    # Check if a specific treatment is pre-selected
    selected_treatment_id = request.GET.get('treatment')
    selected_treatment = None
    if selected_treatment_id:
        try:
            selected_treatment = Treatment.objects.get(id=selected_treatment_id)  # type: ignore
        except Treatment.DoesNotExist:  # type: ignore
            pass
    
    context = {
        'treatments': treatments,
        'selected_treatment': selected_treatment
    }
    
    if request.method == 'POST':
        # Process the booking form submission
        try:
            # Get form data
            treatment_id = request.POST.get('treatment_id')
            doctor_id = request.POST.get('doctor_id')
            hospital_id = request.POST.get('hospital_id')
            preferred_date = request.POST.get('preferred_date')
            total_amount = request.POST.get('total_amount')
            agree_terms = request.POST.get('agree_terms')
            
            # Validate required fields
            if not all([treatment_id, hospital_id, total_amount]):
                messages.error(request, 'Please complete all required steps in the booking process.')
                return render(request, "bookings/new_booking.html", context)
            
            if not agree_terms:
                messages.error(request, 'You must agree to the Terms of Service and Privacy Policy.')
                return render(request, "bookings/new_booking.html", context)
            
            # Get the objects
            treatment = get_object_or_404(Treatment, id=treatment_id)
            hospital = get_object_or_404(Hospital, id=hospital_id)
            doctor = None
            if doctor_id:
                doctor = get_object_or_404(Doctor, id=doctor_id)
            
            # Create a booking record in the database
            # Get or create user profile
            user_profile = None
            if hasattr(request, 'user') and request.user.is_authenticated:  # type: ignore
                # Try to get existing user profile
                try:
                    user_profile = request.user.userprofile  # type: ignore
                except AttributeError:
                    # If user profile doesn't exist, we'll create booking without it
                    user_profile = None
                except Exception:
                    # Handle any other exception
                    user_profile = None
            
            # Create booking
            booking = Booking(
                treatment=treatment,
                preferred_doctor=doctor,
                preferred_hospital=hospital,
                patient=user_profile,
                preferred_date=preferred_date if preferred_date else None,
                status='pending',
                amount=Decimal(str(total_amount))
            )
            
            booking.save()  # type: ignore
            
            # Redirect to payment page
            return redirect('payments:booking_payment', booking_id=booking.id)  # type: ignore
            
        except Exception as e:
            logger.error(f"Error processing booking: {str(e)}", exc_info=True)
            messages.error(request, 'An error occurred while processing your booking request. Please try again.')
    
    return render(request, "bookings/new_booking.html", context)


@require_http_methods(["GET"])
def get_doctors_by_treatment(request: HttpRequest, treatment_id: int) -> JsonResponse:
    """API endpoint to get doctors by treatment"""
    try:
        treatment = Treatment.objects.get(id=treatment_id)  # type: ignore
        doctors = treatment.doctors.all().order_by('name')  # type: ignore
        
        doctors_data = []
        for doctor in doctors:
            doctors_data.append({
                'id': doctor.id,
                'name': doctor.name,
                'specialization': doctor.specialization,
                'rating': float(doctor.rating) if doctor.rating else 0,
                'review_count': doctor.review_count,
            })
        
        return JsonResponse({
            'success': True,
            'doctors': doctors_data
        })
    except Treatment.DoesNotExist:  # type: ignore
        return JsonResponse({
            'success': False,
            'error': 'Treatment not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error getting doctors by treatment ID {treatment_id}: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'An error occurred while fetching doctors: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_hospitals_by_treatment(request: HttpRequest, treatment_id: int) -> JsonResponse:
    """API endpoint to get hospitals by treatment"""
    try:
        treatment = Treatment.objects.get(id=treatment_id)  # type: ignore
        hospitals = treatment.hospitals.all().order_by('name')  # type: ignore
        
        hospitals_data = []
        for hospital in hospitals:
            hospitals_data.append({
                'id': hospital.id,
                'name': hospital.name,
                'slug': hospital.slug,
                'city': hospital.city,
                'state': hospital.state.name if hospital.state else '',
                'country': hospital.country.name if hospital.country else '',
                'rating': float(hospital.rating) if hospital.rating else 0,
                'starting_price': float(hospital.starting_price) if hospital.starting_price else 0,
                'is_takeopinion_choice': hospital.is_takeopinion_choice,
                'jci_accredited': hospital.jci_accredited,
                'nabh_accredited': hospital.nabh_accredited,
                'iso_certified': hospital.iso_certified,
                'profile_picture': hospital.profile_picture,  # Add profile picture URL
            })
        
        return JsonResponse({
            'success': True,
            'hospitals': hospitals_data
        })
    except Treatment.DoesNotExist:  # type: ignore
        return JsonResponse({
            'success': False,
            'error': 'Treatment not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error getting hospitals by treatment: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while fetching hospitals'
        }, status=500)


@require_http_methods(["GET"])
def get_rooms_by_hospital(request: HttpRequest, hospital_id: int) -> JsonResponse:
    """API endpoint to get room options by hospital"""
    try:
        hospital = Hospital.objects.get(id=hospital_id)  # type: ignore
        accommodations = hospital.accommodations.all().order_by('price_per_night')  # type: ignore
        
        rooms_data = []
        for accommodation in accommodations:
            rooms_data.append({
                'id': accommodation.id,
                'name': accommodation.name,
                'price_per_night': float(accommodation.price_per_night),
                'address': accommodation.address,
            })
        
        # If no accommodations found, provide default room options
        if not rooms_data:
            rooms_data = [
                {
                    'id': 1,
                    'name': 'Standard Room',
                    'price_per_night': 2500.00,
                    'address': 'Included with hospital stay',
                },
                {
                    'id': 2,
                    'name': 'Deluxe Room',
                    'price_per_night': 4500.00,
                    'address': 'Included with hospital stay',
                },
                {
                    'id': 3,
                    'name': 'Suite',
                    'price_per_night': 8000.00,
                    'address': 'Included with hospital stay',
                }
            ]
        
        return JsonResponse({
            'success': True,
            'rooms': rooms_data
        })
    except Hospital.DoesNotExist:  # type: ignore
        return JsonResponse({
            'success': False,
            'error': 'Hospital not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error getting rooms by hospital: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while fetching room options'
        }, status=500)


@require_http_methods(["GET"])
def get_doctor_pricing(request: HttpRequest, doctor_id: int, treatment_id: int, hospital_id: int) -> JsonResponse:
    """API endpoint to get pricing for a doctor's treatment at a specific hospital"""
    try:
        doctor = Doctor.objects.get(id=doctor_id)  # type: ignore
        price = doctor.get_treatment_price_at_hospital(treatment_id, hospital_id)
        
        if price is not None:
            return JsonResponse({
                'success': True,
                'price': price,
                'message': f"Doctor {doctor.name} offers this treatment at this hospital for ₹{price}"
            })
        else:
            # Return the hospital's general pricing if doctor-specific pricing is not available
            hospital = Hospital.objects.get(id=hospital_id)  # type: ignore
            treatment = Treatment.objects.get(id=treatment_id)  # type: ignore
            general_price = float(hospital.starting_price)
            
            return JsonResponse({
                'success': True,
                'price': general_price,
                'message': f"Hospital pricing for {treatment.name} at {hospital.name}: ₹{general_price}"
            })
    except (Doctor.DoesNotExist, Hospital.DoesNotExist, Treatment.DoesNotExist):  # type: ignore
        return JsonResponse({
            'success': False,
            'error': 'Doctor, hospital, or treatment not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error getting doctor pricing: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while fetching pricing information'
        }, status=500)


@require_http_methods(["GET"])
def get_treatment_pricing(request: HttpRequest, treatment_id: int) -> JsonResponse:
    """API endpoint to get general pricing information for a treatment"""
    try:
        treatment = Treatment.objects.get(id=treatment_id)  # type: ignore
        
        # Get hospitals offering this treatment and their prices
        hospitals = treatment.hospitals.all()  # type: ignore
        hospital_prices = []
        
        for hospital in hospitals:
            hospital_prices.append({
                'id': hospital.id,
                'name': hospital.name,
                'price': float(hospital.starting_price),
                'city': hospital.city,
                'rating': float(hospital.rating) if hospital.rating else 0
            })
        
        return JsonResponse({
            'success': True,
            'treatment': {
                'id': treatment.id,
                'name': treatment.name,
                'description': treatment.description,
                'starting_price': float(treatment.starting_price),
            },
            'hospitals': hospital_prices
        })
    except Treatment.DoesNotExist:  # type: ignore
        return JsonResponse({
            'success': False,
            'error': 'Treatment not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error getting treatment pricing: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while fetching treatment pricing information'
        }, status=500)


def booking_page(request: HttpRequest) -> HttpResponse:
    # Get all treatments, doctors, and hospitals for the dropdowns
    treatments = Treatment.objects.all().order_by('name')  # type: ignore
    doctors = Doctor.objects.all().order_by('name')  # type: ignore
    hospitals = Hospital.objects.all().order_by('name')  # type: ignore
    
    # Check if a specific doctor is selected
    selected_doctor_id = request.GET.get('doctor')
    selected_doctor = None
    if selected_doctor_id:
        try:
            selected_doctor = Doctor.objects.get(id=selected_doctor_id)  # type: ignore
            # Filter treatments to only those offered by this doctor
            treatments = selected_doctor.treatments.all().order_by('name')  # type: ignore
        except Doctor.DoesNotExist:  # type: ignore
            pass
    
    # Check if a specific treatment is selected
    selected_treatment_id = request.GET.get('treatment')
    selected_treatment = None
    if selected_treatment_id:
        try:
            selected_treatment = Treatment.objects.get(id=selected_treatment_id)  # type: ignore
            # Filter doctors and hospitals to only those offering this treatment
            doctors = selected_treatment.doctors.all().order_by('name')  # type: ignore
            hospitals = selected_treatment.hospitals.all().order_by('name')  # type: ignore
        except Treatment.DoesNotExist:  # type: ignore
            pass
    
    context = {
        'treatments': treatments,
        'doctors': doctors,
        'hospitals': hospitals,
        'selected_doctor': selected_doctor,
        'selected_treatment': selected_treatment
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
            total_cost = request.POST.get('total_cost')  # Changed from budget to total_cost
            medical_history = request.POST.get('medical_history')
            travel_companions = request.POST.get('travel_companions')
            urgency = request.POST.get('urgency')
            agree_terms = request.POST.get('agree_terms')
            notes = request.POST.get('notes')
            
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
            elif selected_doctor:
                preferred_doctor = selected_doctor
            
            if preferred_hospital_id:
                preferred_hospital = get_object_or_404(Hospital, id=preferred_hospital_id)
            
            # Create a booking record in the database
            # Get or create user profile
            user_profile = None
            if hasattr(request, 'user') and request.user.is_authenticated:  # type: ignore
                # Try to get existing user profile
                try:
                    user_profile = request.user.userprofile  # type: ignore
                except AttributeError:
                    # If user profile doesn't exist, we'll create booking without it
                    user_profile = None
                except Exception:
                    # Handle any other exception
                    user_profile = None
            
            # Create booking
            booking = Booking(
                treatment=treatment,
                preferred_doctor=preferred_doctor,
                preferred_hospital=preferred_hospital,
                patient=user_profile,
                preferred_date=preferred_date if preferred_date else None,
                status='pending',
                notes=notes
            )
            
            # Set amount - use total_cost from form or fallback to treatment price
            if total_cost:
                booking.amount = Decimal(str(total_cost))  # type: ignore
            else:
                booking.amount = treatment.starting_price  # type: ignore
            
            booking.save()  # type: ignore
            
            # Handle medical report uploads
            medical_reports = request.FILES.getlist('medical_reports')
            if medical_reports:
                # Save booking first to get its id
                booking_id = booking.id  # type: ignore
                for uploaded_file in medical_reports:
                    MedicalReport(
                        booking=booking,
                        file=uploaded_file,
                        description=f"Medical report uploaded for booking #{booking_id}"
                    ).save()
            
            # Redirect to payment page instead of confirmation page
            # Redirect to home page with success message
            booking_id = booking.id  # type: ignore
            messages.success(request, f'Your booking has been confirmed successfully! Booking ID: {booking_id}. Our team will contact you shortly to finalize the details.')
            return redirect('home')
            
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
        notes = request.POST.get('notes')
        
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
                try:
                    category = TreatmentCategory._default_manager.get(name="General")
                except Exception:
                    category = TreatmentCategory._default_manager.create(
                        name="General",
                        type="medical"
                    )
                
                try:
                    treatment = Treatment._default_manager.get(name="General Consultation")
                except Exception:
                    treatment = Treatment._default_manager.create(
                        name="General Consultation",
                        description="General medical consultation",
                        category=category,
                        starting_price=50.00
                    )
            
            # Generate Google Meet link (in a real implementation, this would use Google Calendar API)
            meet_link = f"https://meet.google.com/{uuid.uuid4().hex[:3]}-{uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:3]}"
            
            # Create booking
            booking = Booking(
                treatment=treatment,
                preferred_doctor=doctor,
                patient=None,  # Default to None
                preferred_date=preferred_date,
                status='pending',
                google_meet_link=meet_link if consultation_type == 'video' else None,
                notes=notes
            )  # type: ignore
            
            # Try to assign patient profile if user is authenticated
            if hasattr(request, 'user') and request.user.is_authenticated:  # type: ignore
                try:
                    booking.patient = request.user.userprofile  # type: ignore
                except AttributeError:
                    # If user profile doesn't exist, leave as None
                    pass
                except Exception:
                    # Handle any other exception
                    pass
            
            # Set amount
            if treatment:
                booking.amount = treatment.starting_price  # type: ignore
            else:
                booking.amount = Decimal('50.00')  # type: ignore
            
            booking.save()  # type: ignore
            
            # Handle medical report uploads
            medical_reports = request.FILES.getlist('medical_reports')
            if medical_reports:
                # Save booking first to get its id
                booking_id = booking.id  # type: ignore
                for uploaded_file in medical_reports:
                    MedicalReport(
                        booking=booking,
                        file=uploaded_file,
                        description=f"Medical report uploaded for consultation booking #{booking_id}"
                    ).save()
            
            # Store consultation details for later use
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
            
            # Redirect to payment page
            return redirect('payments:consultation_payment', booking_id=booking.id)  # type: ignore
            
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


def payment_page(request: HttpRequest, booking_id: int) -> HttpResponse:
    """Display payment page for the booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    context = {
        'booking': booking,
        'amount': booking.amount,
    }
    
    # Redirect to static payment demo instead of Razorpay
    return redirect('payments:static_payment_demo', booking_id=booking_id)


@login_required
def admin_dashboard(request):
    """Admin dashboard to manage appointments"""
    # Check if user is admin
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    # Get all bookings with patient information
    # Using _default_manager as a workaround for typing issues
    bookings = Booking._default_manager.select_related('patient__user', 'treatment', 'preferred_doctor', 'preferred_hospital').all().order_by('-created_at')
    
    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Calculate statistics
    total_bookings = bookings.count()
    pending_bookings = bookings.filter(status='pending').count()
    confirmed_bookings = bookings.filter(status='confirmed').count()
    cancelled_bookings = bookings.filter(status='cancelled').count()
    in_progress_bookings = bookings.filter(status='in_progress').count()
    completed_bookings = bookings.filter(status='completed').count()
    
    # Calculate today's bookings
    from django.utils import timezone
    from datetime import date
    today = date.today()
    today_bookings = bookings.filter(created_at__date=today).count()
    
    # Get recent bookings (last 5)
    recent_bookings = bookings[:5]
    
    # Get top treatments
    from django.db.models import Count
    top_treatments = bookings.filter(treatment__isnull=False).values('treatment__name').annotate(count=Count('treatment')).order_by('-count')[:5]
    
    # Calculate booking trends (last 7 days)
    from datetime import timedelta
    week_ago = today - timedelta(days=7)
    weekly_bookings = bookings.filter(created_at__date__gte=week_ago).extra({'date': 'date(created_at)'}).values('date').annotate(count=Count('id')).order_by('date')
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'in_progress_bookings': in_progress_bookings,
        'completed_bookings': completed_bookings,
        'today_bookings': today_bookings,
        'recent_bookings': recent_bookings,
        'top_treatments': top_treatments,
        'weekly_bookings': weekly_bookings,
    }
    
    return render(request, "bookings/admin_dashboard.html", context)


@login_required
def update_booking_status(request, booking_id, status):
    """Update booking status (accept/reject)"""
    # Check if user is admin
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('home')
    
    # Get the booking
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Validate status - accept all valid status values
    valid_statuses = ['pending', 'confirmed', 'in_progress', 'completed', 'cancelled']
    if status in valid_statuses:
        booking.status = status
        booking.save()
        messages.success(request, f'Booking #{booking.id} has been updated to {status.replace("_", " ").title()}.')
    else:
        messages.error(request, 'Invalid status update.')
    
    return redirect('bookings:admin_dashboard')


@login_required
def join_consultation(request, booking_id):
    """Redirect doctor to Google Meet link for video consultation"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user is authorized (doctor or admin)
    user_profile = getattr(request.user, 'userprofile', None)
    if not user_profile:
        messages.error(request, 'You must be logged in to join a consultation.')
        return redirect('accounts:login')
    
    # Check if user is the assigned doctor or an admin
    is_authorized = (
        (user_profile.user_type == 'doctor' and booking.preferred_doctor and 
         hasattr(request.user, 'doctor') and request.user.doctor == booking.preferred_doctor) or
        user_profile.user_type == 'admin'
    )
    
    if not is_authorized:
        messages.error(request, 'You are not authorized to join this consultation.')
        return redirect('home')
    
    # Check if this is a video consultation with a Google Meet link
    if not booking.google_meet_link:
        messages.error(request, 'This is not a video consultation or the meeting link is not available.')
        return redirect('home')
    
    # Redirect to Google Meet
    return redirect(booking.google_meet_link)

@require_http_methods(["GET"])
def get_hospitals_by_treatment_and_doctor(request: HttpRequest, treatment_id: int, doctor_id: int) -> JsonResponse:
    """API endpoint to get hospitals by treatment and doctor (hospitals where the doctor works and offers the treatment)"""
    try:
        treatment = Treatment.objects.get(id=treatment_id)  # type: ignore
        doctor = Doctor.objects.get(id=doctor_id)  # type: ignore
        
        # Get hospitals that offer this treatment AND employ this doctor
        hospitals = Hospital.objects.filter(
            treatments=treatment,
            doctors=doctor
        ).order_by('name')  # type: ignore
        
        hospitals_data = []
        for hospital in hospitals:
            hospitals_data.append({
                'id': hospital.id,
                'name': hospital.name,
                'city': hospital.city,
                'state': hospital.state.name if hospital.state else '',
                'country': hospital.country.name if hospital.country else '',
                'rating': float(hospital.rating) if hospital.rating else 0,
                'starting_price': float(hospital.starting_price) if hospital.starting_price else 0,
                'is_takeopinion_choice': hospital.is_takeopinion_choice,
                'jci_accredited': hospital.jci_accredited,
                'nabh_accredited': hospital.nabh_accredited,
                'iso_certified': hospital.iso_certified,
                'slug': hospital.slug,
                'profile_picture': hospital.profile_picture,  # Add profile picture URL
            })
        
        return JsonResponse({
            'success': True,
            'hospitals': hospitals_data
        })
    except (Treatment.DoesNotExist, Doctor.DoesNotExist):  # type: ignore
        return JsonResponse({
            'success': False,
            'error': 'Treatment or doctor not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error getting hospitals by treatment and doctor: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while fetching hospitals'
        }, status=500)
