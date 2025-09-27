from django.db import models
from treatments.models import Treatment
from doctors.models import Doctor
from hospitals.models import Hospital
from accounts.models import UserProfile


class Booking(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    preferred_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings', null=True)
    preferred_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self) -> str:
        return f"Booking for {self.treatment.name}"


class Accommodation(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="accommodations")
    name = models.CharField(max_length=200)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    address = models.CharField(max_length=250, blank=True)

    def __str__(self) -> str:
        return f"{self.name} near {self.hospital.name}"

# Create your models here.