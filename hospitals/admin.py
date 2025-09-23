from django.contrib import admin
from .models import Hospital, HospitalMedia


class HospitalMediaInline(admin.TabularInline):
    model = HospitalMedia
    extra = 1


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "city", "country", "state", "rating", "is_takeopinion_choice")
    list_filter = ("country", "state", "is_takeopinion_choice")
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'about', 'rating', 'is_takeopinion_choice', 'profile_picture')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'country')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Hospital Details', {
            'fields': ('established_year', 'beds_count', 'staff_count', 'departments_count', 'awards_count')
        }),
        ('Certifications', {
            'fields': ('jci_accredited', 'nabh_accredited', 'iso_certified')
        }),
        ('Treatments', {
            'fields': ('treatments',)
        }),
    )
    inlines = [HospitalMediaInline]


@admin.register(HospitalMedia)
class HospitalMediaAdmin(admin.ModelAdmin):
    list_display = ("hospital", "image_url")

# Register your models here.