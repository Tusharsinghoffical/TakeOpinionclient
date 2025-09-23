from django.test import TestCase
from django.contrib.auth.models import User
from .models import Doctor, DoctorMedia


class DoctorMediaModelTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            name="Dr. Test Doctor",
            specialization="Test Specialization"
        )
        self.media = DoctorMedia.objects.create(
            doctor=self.doctor,
            image_url="https://example.com/test-image.jpg"
        )

    def test_doctor_media_creation(self):
        """Test that DoctorMedia objects can be created"""
        self.assertEqual(self.media.doctor, self.doctor)
        self.assertEqual(self.media.image_url, "https://example.com/test-image.jpg")
        
    def test_doctor_media_str_representation(self):
        """Test the string representation of DoctorMedia"""
        expected_str = f"Media for {self.doctor.name}"
        self.assertEqual(str(self.media), expected_str)
        
    def test_doctor_media_relationship(self):
        """Test that media items are properly related to doctors"""
        media_items = self.doctor.media_items.all()
        self.assertEqual(media_items.count(), 1)
        self.assertEqual(media_items.first(), self.media)