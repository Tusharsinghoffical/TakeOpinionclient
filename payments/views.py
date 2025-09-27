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


@login_required
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


@login_required
def process_static_payment(request, booking_id):
    """Process static payment demo and show success page"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Create a payment record to simulate real payment processing
    payment = Payment(
        booking=booking,
        user=request.user.userprofile,
        amount=booking.treatment.starting_price,
        currency='INR',
        status='completed'
    )
    payment.save()
    
    # Update booking status to confirmed
    booking.status = 'confirmed'
    booking.save()
    
    # Redirect to payment success page
    return redirect('payments:static_payment_success', payment_id=payment.id)


@login_required
def static_payment_success(request, payment_id):
    """Display static payment success page"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    context = {
        'payment': payment,
    }
    
    return render(request, 'payments/static_success.html', context)