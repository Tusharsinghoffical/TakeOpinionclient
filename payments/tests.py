from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfile
from bookings.models import Booking
from treatments.models import Treatment, TreatmentCategory
from .models import Payment


class PaymentModelTest(TestCase):
    def setUp(self):
        # Create a user and user profile
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_type='patient'
        )
        
        # Create a treatment category and treatment
        self.category = TreatmentCategory.objects.create(
            name='Test Category',
            type='medical'
        )
        self.treatment = Treatment.objects.create(
            name='Test Treatment',
            description='Test Description',
            category=self.category
        )
        
        # Create a booking
        self.booking = Booking.objects.create(
            treatment=self.treatment,
            patient=self.user_profile,
            amount=5000.00,
            status='pending'
        )
    
    def test_payment_creation(self):
        """Test that a payment can be created"""
        payment = Payment.objects.create(
            booking=self.booking,
            user=self.user_profile,
            amount=5000.00,
            currency='INR',
            status='pending'
        )
        
        self.assertEqual(payment.booking, self.booking)
        self.assertEqual(payment.user, self.user_profile)
        self.assertEqual(payment.amount, 5000.00)
        self.assertEqual(payment.currency, 'INR')
        self.assertEqual(payment.status, 'pending')
    
    def test_payment_string_representation(self):
        """Test the string representation of a payment"""
        payment = Payment.objects.create(
            booking=self.booking,
            user=self.user_profile,
            amount=5000.00,
            currency='INR',
            status='pending'
        )
        
        expected_string = f"Payment for booking {payment.booking.id} - pending"
        self.assertEqual(str(payment), expected_string)