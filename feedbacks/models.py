from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile
from treatments.models import Treatment
from hospitals.models import Hospital
from doctors.models import Doctor

class Feedback(models.Model):
    """Model to store patient feedback for doctors, hospitals, and treatments."""
    
    # Feedback types
    FEEDBACK_TYPE_CHOICES = [
        ('doctor', 'Doctor'),
        ('hospital', 'Hospital'),
        ('treatment', 'Treatment'),
    ]
    
    # Rating choices
    RATING_CHOICES = [
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]
    
    # Core fields
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
    
    # Related entities (only one will be populated based on feedback_type)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacks')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacks')
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacks')
    
    # Feedback content
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    video_url = models.URLField(blank=True, null=True)  # For storing video review URLs
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status - Changed default to True so reviews are immediately visible
    is_approved = models.BooleanField(default=True, help_text="Feedback is immediately public")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
    
    def __str__(self):
        return f"{self.get_feedback_type_display()}: {self.title} by {self.patient.user.username}"
    
    def save(self, *args, **kwargs):
        # Ensure only the relevant foreign key is set based on feedback_type
        if self.feedback_type == 'doctor':
            self.hospital = None
            self.treatment = None
        elif self.feedback_type == 'hospital':
            self.doctor = None
            self.treatment = None
        elif self.feedback_type == 'treatment':
            self.doctor = None
            self.hospital = None
        super().save(*args, **kwargs)