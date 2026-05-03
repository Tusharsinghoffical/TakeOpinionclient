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


def booking_payment(request, booking_id):
    """Display booking payment page"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Calculate amount with service charge and tax
    if booking.treatment:
        # Base amount from treatment
        base_amount = float(booking.treatment.starting_price)
        # Add service charge (10%)
        service_charge = base_amount * 0.10
        # Add tax (18% on total of base + service charge)
        tax = (base_amount + service_charge) * 0.18
        # Total amount
        amount = base_amount + service_charge + tax
    else:
        base_amount = 1947.00
        service_charge = base_amount * 0.10
        tax = (base_amount + service_charge) * 0.18
        amount = base_amount + service_charge + tax
    
    # Round all values to 2 decimal places for display
    context = {
        'booking': booking,
        'amount': round(amount, 2),
        'base_amount': round(base_amount, 2),
        'service_charge': round(service_charge, 2),
        'tax': round(tax, 2),
    }
    
    return render(request, 'payments/booking_payment.html', context)


def consultation_payment(request, booking_id):
    """Display consultation payment page"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # For consultation, we use a fixed amount or treatment price
    amount = 1947.00  # Fixed consultation amount with taxes
    
    # If booking has a treatment, use its price
    if booking.treatment:
        # Base amount from treatment
        base_amount = float(booking.treatment.starting_price)
        # Add service charge (10%)
        service_charge = base_amount * 0.10
        # Add tax (18% on total)
        tax = (base_amount + service_charge) * 0.18
        # Total amount
        amount = base_amount + service_charge + tax
    
    context = {
        'booking': booking,
        'amount': round(amount, 2),
    }
    
    return render(request, 'payments/consultation_payment.html', context)


def static_payment_demo(request, booking_id):
    """Display static payment demo page"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Calculate amount (this would normally come from the treatment pricing)
    amount = float(booking.treatment.starting_price) if booking.treatment else 1947.00
    
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
    
    # Calculate amount for the booking
    if booking.treatment:
        # Base amount from treatment
        base_amount = float(booking.treatment.starting_price)
        # Add service charge (10%)
        service_charge = base_amount * 0.10
        # Add tax (18% on total)
        tax = (base_amount + service_charge) * 0.18
        # Total amount
        amount = base_amount + service_charge + tax
    else:
        # Default amount if no treatment
        amount = 1947.00
    
    # Create a payment record to simulate real payment processing
    payment = Payment(
        booking=booking,
        user=user,  # Use the authenticated user if available
        amount=round(amount, 2),  # Use calculated amount
        currency='INR',  # Changed to INR to match the UI
        status='completed'
    )
    payment.save()
    
    # Update booking status to confirmed
    booking.status = 'confirmed'
    booking.save()
    
    # Check if this is a consultation booking (has a doctor and Google Meet link)
    if booking.preferred_doctor and booking.google_meet_link:
        # Redirect to consultation confirmation page
        return redirect('payments:consultation_payment_success', payment_id=payment.pk)
    else:
        # Redirect to booking success page
        return redirect('payments:booking_success', payment_id=payment.pk)


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
    
    return render(request, 'payments/consultation_success.html', context)


@login_required
def booking_success(request, payment_id):
    """Display booking payment success page"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    context = {
        'payment': payment,
    }
    
    return render(request, 'payments/booking_success.html', context)


@login_required
def static_payment_success(request, payment_id):
    """Display static payment success page"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    context = {
        'payment': payment,
    }
    
    return render(request, 'payments/static_success.html', context)