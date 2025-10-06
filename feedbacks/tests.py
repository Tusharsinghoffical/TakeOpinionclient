from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import UserProfile, PatientProfile
from feedbacks.models import Feedback
from doctors.models import Doctor
from hospitals.models import Hospital
from treatments.models import Treatment, TreatmentCategory

class ReviewsPageTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testpatient',
            password='testpass123'
        )
        
        # Create user profile
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_type='patient'
        )
        
        # Create patient profile
        self.patient_profile = PatientProfile.objects.create(
            user_profile=self.user_profile
        )
        
        # Create test entities
        self.doctor = Doctor.objects.create(
            name='Dr. Test Doctor',
            specialization='Test Specialization'
        )
        
        self.hospital = Hospital.objects.create(
            name='Test Hospital',
            city='Test City'
        )
        
        # Create a treatment category first
        self.treatment_category = TreatmentCategory.objects.create(
            name='Test Category',
            type='medical'
        )
        
        self.treatment = Treatment.objects.create(
            name='Test Treatment',
            description='Test Description',
            category=self.treatment_category
        )
        
        # Create test feedback
        self.feedback = Feedback.objects.create(
            patient=self.user_profile,
            feedback_type='doctor',
            doctor=self.doctor,
            rating=5,
            title='Great Doctor',
            comment='Excellent service',
            is_approved=True
        )
        
        self.client = Client()

    def test_reviews_page_loads(self):
        """Test that the reviews page loads successfully"""
        response = self.client.get('/accounts/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Patient Reviews')
        
    def test_reviews_page_requires_no_login(self):
        """Test that the reviews page is accessible without login"""
        response = self.client.get('/accounts/reviews/')
        self.assertEqual(response.status_code, 200)
        
    def test_reviews_display(self):
        """Test that reviews are displayed on the page"""
        response = self.client.get('/accounts/reviews/')
        self.assertContains(response, 'Great Doctor')
        self.assertContains(response, 'Excellent service')
        
    def test_write_review_button_for_authenticated_patients(self):
        """Test that authenticated patients see the write review button"""
        self.client.login(username='testpatient', password='testpass123')
        response = self.client.get('/accounts/reviews/')
        self.assertContains(response, 'Write a Review')
        
    def test_login_button_for_non_authenticated_users(self):
        """Test that non-authenticated users see the login button"""
        response = self.client.get('/accounts/reviews/')
        self.assertContains(response, 'Login to Write a Review')