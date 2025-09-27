# Razorpay Payment Integration Guide

## Overview
This document explains how to integrate and use the Razorpay payment system in the TakeOpinion application.

## Setup Instructions

### 1. Environment Variables
Add the following environment variables to your `.env` file or system environment:

```bash
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

For development, you can use test keys from your Razorpay dashboard:
- Test Key ID: `rzp_test_XXXXXXXXXXXXXX`
- Test Key Secret: `XXXXXXXXXXXXXXXXXXXXXXXX`

### 2. Dependencies
The required dependencies are already included in `requirements.txt`:
- `razorpay==1.4.2`

### 3. Database Migration
The payment system requires a database migration to create the Payment model:

```bash
python manage.py makemigrations payments
python manage.py migrate
```

## Integration Flow

### 1. Creating a Payment Order
To initiate a payment, make a POST request to `/payments/create-order/` with the following data:

```json
{
  "booking_id": 1,
  "amount": 5000.00
}
```

This will return a response with the Razorpay order details:

```json
{
  "order_id": "order_XXXXXXXXXXXX",
  "amount": 5000.00,
  "currency": "INR",
  "razorpay_key": "rzp_test_XXXXXXXXXXXXXX",
  "booking_id": 1
}
```

### 2. Razorpay Checkout
The frontend uses the returned order details to initialize the Razorpay checkout:

```javascript
var options = {
  "key": "{{ razorpay_key }}",
  "amount": "{{ amount_in_paise }}",
  "currency": "{{ currency }}",
  "name": "TakeOpinion",
  "description": "Payment for {{ booking.treatment.name }}",
  "order_id": "{{ order_id }}",
  "handler": function (response){
    // Verify payment on server
    fetch("/payments/verify-payment/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'
      },
      body: JSON.stringify({
        'razorpay_payment_id': response.razorpay_payment_id,
        'razorpay_order_id': response.razorpay_order_id,
        'razorpay_signature': response.razorpay_signature
      })
    })
  }
}
```

### 3. Payment Verification
After successful payment, Razorpay redirects to the verification endpoint which:
1. Verifies the payment signature
2. Updates the payment status in the database
3. Updates the booking status to 'confirmed'

### 4. Success/Failure Handling
Based on verification results, users are redirected to:
- Success page: `/payments/payment-success/`
- Failure page: `/payments/payment-failure/`

## Models

### Payment Model
The Payment model stores all payment-related information:

```python
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='payments')
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## URLs

The payment system provides the following endpoints:

- `POST /payments/create-order/` - Create a Razorpay order
- `POST /payments/verify-payment/` - Verify payment signature
- `GET /payments/payment-success/` - Payment success page
- `GET /payments/payment-failure/` - Payment failure page

## Security Considerations

1. All payment endpoints use CSRF protection
2. Payment verification uses Razorpay's official signature verification
3. Sensitive payment data is stored securely in the database
4. Only authenticated users can initiate payments

## Testing

Run the payment tests with:

```bash
python manage.py test payments
```

The test suite includes:
- Payment model creation and validation
- String representation of payment objects

## Troubleshooting

### Common Issues

1. **Signature Verification Failed**
   - Ensure the correct key secret is used
   - Check that the order ID matches the one created

2. **Database Migration Issues**
   - Run `python manage.py migrate` to apply pending migrations

3. **Environment Variables Not Set**
   - Check that `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` are properly configured

### Logging
Payment-related errors are logged using Django's logging system. Check the logs for detailed error information.