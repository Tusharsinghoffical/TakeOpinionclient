from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor


class SharedReport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('viewed', 'Viewed'),
        ('replied', 'Replied'),
    ]

    # Sender (patient — can be anonymous guest or logged-in user)
    sender_name  = models.CharField(max_length=100)
    sender_email = models.EmailField()
    sender_user  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_reports')

    # Target doctor
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='shared_reports')

    # Report file
    report_file = models.FileField(upload_to='shared_reports/')
    report_name = models.CharField(max_length=255, blank=True)
    notes       = models.TextField(blank=True, help_text="Patient's note to the doctor")

    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report from {self.sender_name} to Dr. {self.doctor.name}"


class ReportMessage(models.Model):
    report     = models.ForeignKey(SharedReport, on_delete=models.CASCADE, related_name='messages')
    sender     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sender_name = models.CharField(max_length=100)   # fallback for guests
    is_doctor  = models.BooleanField(default=False)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message on report #{self.report.id} by {self.sender_name}"
