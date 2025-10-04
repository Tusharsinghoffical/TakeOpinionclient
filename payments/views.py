import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import Payment
from bookings.models import Booking
from django.urls import reverse

# Configure logging
logger = logging.getLogger(__name__)


@login_required
def payment_success(request):
    """Display payment success page and redirect to hotel suggestions"""
    # For static payment, we redirect directly to hotel suggestions
    # This view is kept for backward compatibility
    messages.info(request, 'Payment processed successfully!')
    return redirect('accounts:admin_dashboard')


def static_payment_demo(request, booking_id):
    """Display static payment demo page"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Calculate amount (this would normally come from the treatment pricing)
    amount = booking.treatment.starting_price
    
    context = {
        'booking': booking,
        'amount': amount,
    }
    
    return render(request, 'payments/static_payment.html', context)


def process_static_payment(request, booking_id):
    """Process static payment demo and show success page"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Determine the user for the payment
    user = None
    if request.user.is_authenticated:
        try:
            user = request.user.userprofile
        except AttributeError:
            # If user profile doesn't exist, leave user as None
            pass
    
    # Create a payment record to simulate real payment processing
    payment = Payment(
        booking=booking,
        user=user,  # Use the authenticated user if available
        amount=booking.treatment.starting_price,
        currency='INR',
        status='completed'
    )
    payment.save()
    
    # Update booking status to confirmed
    booking.status = 'confirmed'
    booking.save()
    
    # Check if this is a consultation booking (has a doctor)
    if booking.preferred_doctor:
        # Redirect to consultation confirmation page
        return redirect('payments:consultation_payment_success', payment_id=payment.pk)
    else:
        # Redirect to regular payment success page
        return redirect('payments:static_payment_success', payment_id=payment.pk)


@login_required
def consultation_payment_success(request, payment_id):
    """Display consultation payment success page with Google Meet link"""
    payment = get_object_or_404(Payment, id=payment_id)
    booking = payment.booking
    
    # Prepare consultation details
    consultation_details = {
        'type': 'video' if booking.google_meet_link else 'phone',
        'date': booking.preferred_date,
        'time': '10:00 AM',  # This would come from the booking in a real implementation
        'booking_id': booking.id,
        'amount': float(payment.amount)
    }
    
    context = {
        'payment': payment,
        'doctor': booking.preferred_doctor,
        'consultation_details': consultation_details,
        'meet_link': booking.google_meet_link
    }
    
    return render(request, 'bookings/consultation_confirmation.html', context)


@login_required
def static_payment_success(request, payment_id):
    """Display static payment success page"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    context = {
        'payment': payment,
    }
    
    return render(request, 'payments/static_success.html', context)