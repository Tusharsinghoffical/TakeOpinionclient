from django.test import TestCase
from .models import Hospital, HospitalMedia
from core.models import Country


class HospitalMediaModelTest(TestCase):
    def setUp(self):
        # Create a test country
        self.country = Country.objects.create(name="Test Country", code="TC")
        
        # Create a test hospital
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            country=self.country,
            rating=4.5
        )
        
        # Create test media
        self.media = HospitalMedia.objects.create(
            hospital=self.hospital,
            image_url="https://example.com/test-image.jpg"
        )

    def test_hospital_media_creation(self):
        """Test that HospitalMedia objects can be created"""
        self.assertEqual(self.media.hospital, self.hospital)
        self.assertEqual(self.media.image_url, "https://example.com/test-image.jpg")
        
    def test_hospital_media_str_representation(self):
        """Test the string representation of HospitalMedia"""
        expected_str = f"Media for {self.hospital.name}"
        self.assertEqual(str(self.media), expected_str)
        
    def test_hospital_media_relationship(self):
        """Test that media items are properly related to hospitals"""
        media_items = self.hospital.media_items.all()
        self.assertEqual(media_items.count(), 1)
        self.assertEqual(media_items.first(), self.media)