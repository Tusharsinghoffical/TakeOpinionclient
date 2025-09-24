import razorpay
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

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def create_razorpay_order(request):
    """Create a Razorpay order for the booking"""
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")
    
    try:
        # Get booking details from POST data
        booking_id = request.POST.get('booking_id')
        amount = request.POST.get('amount')
        
        if not booking_id or not amount:
            return HttpResponseBadRequest("Missing required parameters")
        
        # Convert amount to paise (smallest currency unit)
        amount_in_paise = int(float(amount) * 100)
        
        # Create Razorpay order
        razorpay_order = client.order.create({
            'amount': amount_in_paise,
            'currency': 'INR',
            'payment_capture': 1  # Auto-capture payment
        })
        
        # Save payment record
        booking = get_object_or_404(Booking, id=booking_id)
        payment = Payment.objects.create(
            booking=booking,
            user=request.user.userprofile,
            razorpay_order_id=razorpay_order['id'],
            amount=amount,
            currency='INR'
        )
        
        # Return order details to frontend
        context = {
            'order_id': razorpay_order['id'],
            'amount': amount,
            'currency': 'INR',
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'booking_id': booking_id,
        }
        
        return JsonResponse(context)
        
    except Exception as e:
        logger.error(f"Error creating Razorpay order: {str(e)}")
        return JsonResponse({'error': 'Failed to create payment order'}, status=500)


@csrf_exempt
def verify_payment(request):
    """Verify the payment using Razorpay's signature verification"""
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")
    
    try:
        # Get payment details from POST data
        payment_data = json.loads(request.body)
        
        razorpay_payment_id = payment_data.get('razorpay_payment_id')
        razorpay_order_id = payment_data.get('razorpay_order_id')
        razorpay_signature = payment_data.get('razorpay_signature')
        
        if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
            return JsonResponse({'error': 'Missing payment details'}, status=400)
        
        # Verify payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
            
            # Update payment record
            payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'completed'
            payment.save()
            
            # Update booking status
            payment.booking.status = 'confirmed'
            payment.booking.save()
            
            return JsonResponse({'status': 'success'})
            
        except razorpay.errors.SignatureVerificationError:
            # Update payment record as failed
            payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)
            payment.status = 'failed'
            payment.save()
            
            return JsonResponse({'status': 'failure'}, status=400)
            
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        return JsonResponse({'error': 'Failed to verify payment'}, status=500)


@login_required
def payment_success(request):
    """Display payment success page"""
    order_id = request.GET.get('order_id')
    
    if not order_id:
        messages.error(request, 'Invalid payment request')
        return redirect('booking_page')
    
    try:
        payment = get_object_or_404(Payment, razorpay_order_id=order_id)
        
        context = {
            'payment': payment,
            'booking': payment.booking,
        }
        
        return render(request, 'payments/success.html', context)
        
    except Exception as e:
        logger.error(f"Error displaying payment success: {str(e)}")
        messages.error(request, 'Error processing payment success')
        return redirect('booking_page')


@login_required
def payment_failure(request):
    """Display payment failure page"""
    order_id = request.GET.get('order_id')
    
    if not order_id:
        messages.error(request, 'Invalid payment request')
        return redirect('booking_page')
    
    try:
        payment = get_object_or_404(Payment, razorpay_order_id=order_id)
        
        context = {
            'payment': payment,
            'booking': payment.booking,
        }
        
        return render(request, 'payments/failure.html', context)
        
    except Exception as e:
        logger.error(f"Error displaying payment failure: {str(e)}")
        messages.error(request, 'Error processing payment failure')
        return redirect('booking_page')