from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, Accommodation


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "get_patient_info", "treatment", "preferred_hospital", "preferred_doctor", "preferred_date", "amount", "status", "created_at")
    list_filter = ("preferred_date", "status", "created_at")
    search_fields = ("id", "patient__user__username", "patient__user__first_name", "patient__user__last_name")
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    @admin.display(description="Patient")
    def get_patient_info(self, obj):
        """Display patient information in the admin list"""
        if obj.patient:
            user = obj.patient.user
            return f"{user.first_name} {user.last_name} ({user.username})"
        else:
            # For appointments booked without user account
            # We'll extract patient name from notes
            if obj.notes and "Appointment for" in obj.notes:
                # Extract patient name from notes
                lines = obj.notes.split('\n')
                for line in lines:
                    if line.startswith("Patient Name:"):
                        return line.replace("Patient Name:", "").strip()
            return "Guest"


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ("name", "hospital", "price_per_night")

# Register your models here.