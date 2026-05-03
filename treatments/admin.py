from django.contrib import admin
from .models import TreatmentCategory, Treatment


@admin.register(TreatmentCategory)
class TreatmentCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "type")


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "category")
    list_filter = ("category__type",)

# Register your models here.
