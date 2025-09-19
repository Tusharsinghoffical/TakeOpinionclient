from django.contrib import admin
from .models import Booking, Accommodation


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "treatment", "preferred_hospital", "preferred_doctor", "preferred_date", "amount")
    list_filter = ("preferred_date",)


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ("name", "hospital", "price_per_night")

# Register your models here.
