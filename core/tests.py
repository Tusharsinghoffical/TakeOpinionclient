from django.test import TestCase, Client
from django.urls import reverse
from treatments.models import Treatment, TreatmentCategory
from doctors.models import Doctor
from hospitals.models import Hospital


class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test data
        category = TreatmentCategory.objects.create(
            name="Test Category",
            type="medical"
        )
        
        self.treatment = Treatment.objects.create(
            name="Test Treatment",
            description="This is a test treatment",
            category=category
        )
        
        self.doctor = Doctor.objects.create(
            name="Test Doctor",
            key_points="Specialist in test treatments"
        )
        
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            about="A hospital for testing purposes"
        )

    def test_search_view_with_query(self):
        response = self.client.get(reverse('search'), {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Treatment')
        self.assertContains(response, 'Test Doctor')
        self.assertContains(response, 'Test Hospital')

    def test_search_view_without_query(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search Results')

    def test_search_view_with_empty_query(self):
        response = self.client.get(reverse('search'), {'q': ''})
        self.assertEqual(response.status_code, 200)