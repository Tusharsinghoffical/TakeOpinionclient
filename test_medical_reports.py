"""
Test script to verify medical reports upload functionality
"""
import os
import django
import uuid
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from bookings.models import Booking, MedicalReport
from treatments.models import Treatment, TreatmentCategory
from doctors.models import Doctor
from accounts.models import UserProfile
from django.contrib.auth.models import User

def test_medical_reports_upload():
    print("Testing medical reports upload functionality...")
    
    # Generate a unique username
    unique_id = uuid.uuid4().hex[:8]
    username = f'testuser_{unique_id}'
    
    # Create a test user
    user = User(
        username=username,
        email=f'test_{unique_id}@example.com'
    )
    user.set_password('testpass123')
    user.save()
    
    # Create a user profile
    user_profile = UserProfile(
        user=user,
        user_type='patient'
    )
    user_profile.save()
    
    # Create a treatment category with unique slug
    category = TreatmentCategory(
        name=f'Test Category {unique_id}',
        type='medical'
    )
    category.slug = slugify(category.name)
    category.save()
    
    # Create a test treatment
    treatment = Treatment(
        name=f'Test Treatment {unique_id}',
        description='Test treatment for medical reports upload',
        starting_price=100.00,
        category=category
    )
    treatment.slug = slugify(treatment.name)
    treatment.save()
    
    # Create a test doctor
    doctor = Doctor(
        name=f'Dr. Test Doctor {unique_id}',
        specialization='Test Specialization'
    )
    doctor.slug = slugify(doctor.name)
    doctor.save()
    
    # Create a test booking
    booking = Booking(
        treatment=treatment,
        preferred_doctor=doctor,
        patient=user_profile,
        status='pending'
    )
    booking.save()
    
    print(f"Created booking #{booking.id}")
    
    # Create test files
    test_files = [
        SimpleUploadedFile("test_report1.pdf", b"PDF content for test report 1", content_type="application/pdf"),
        SimpleUploadedFile("test_report2.jpg", b"JPEG content for test report 2", content_type="image/jpeg"),
        SimpleUploadedFile("test_report3.png", b"PNG content for test report 3", content_type="image/png")
    ]
    
    # Upload medical reports
    for i, uploaded_file in enumerate(test_files):
        medical_report = MedicalReport(
            booking=booking,
            file=uploaded_file,
            description=f"Test medical report {i+1}"
        )
        medical_report.save()
        print(f"Uploaded medical report: {medical_report.file.name}")
    
    # Verify the uploads
    reports = MedicalReport.objects.filter(booking=booking)
    print(f"Total medical reports uploaded: {reports.count()}")
    
    for report in reports:
        print(f"  - {report.file.name}: {report.description}")
    
    # Clean up test data
    for report in reports:
        if report.file:
            report.file.delete()
        report.delete()
    
    booking.delete()
    doctor.delete()
    treatment.delete()
    category.delete()
    user_profile.delete()
    user.delete()
    
    print("Test completed successfully!")

if __name__ == "__main__":
    test_medical_reports_upload()