from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class UserProfile(models.Model):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username


class PatientProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='patient_details')
    medical_history = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    
    def __str__(self):
        return f"Patient: {self.user_profile.user.username}"


class DoctorProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='doctor_details')
    specialization = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Doctor: {self.user_profile.user.username}"