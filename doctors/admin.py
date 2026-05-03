from django.contrib import admin
from .models import Doctor, DoctorMedia


class DoctorMediaInline(admin.TabularInline):
    model = DoctorMedia
    extra = 1


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "specialization", "experience_years", "rating", "review_count")
    list_filter = ("specialization", "experience_years")
    search_fields = ("name", "specialization")
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'specialization', 'about', 'key_points', 'profile_picture')
        }),
        ('Professional Details', {
            'fields': ('education', 'experience_years', 'medical_license_number', 'languages_spoken')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Rating', {
            'fields': ('rating', 'review_count')
        }),
        ('Affiliations', {
            'fields': ('treatments', 'hospitals')
        }),
        ('Awards', {
            'fields': ('awards',)
        }),
    )
    inlines = [DoctorMediaInline]


@admin.register(DoctorMedia)
class DoctorMediaAdmin(admin.ModelAdmin):
    list_display = ("doctor", "image_url")
    search_fields = ("doctor__name",)