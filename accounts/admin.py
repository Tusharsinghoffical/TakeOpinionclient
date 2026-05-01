from django.contrib import admin
from .models import UserProfile, PatientProfile, DoctorProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)