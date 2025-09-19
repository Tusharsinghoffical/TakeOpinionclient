from django.contrib import admin
from .models import Hospital, HospitalMedia


class HospitalMediaInline(admin.TabularInline):
    model = HospitalMedia
    extra = 1


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "country", "state", "rating", "is_takeopinion_choice")
    list_filter = ("country", "state", "is_takeopinion_choice")
    inlines = [HospitalMediaInline]


@admin.register(HospitalMedia)
class HospitalMediaAdmin(admin.ModelAdmin):
    list_display = ("hospital", "image_url", "video_url")

# Register your models here.
