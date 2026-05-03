from django.contrib import admin
from .models import Country, State


# @admin.register(Country)
# class CountryAdmin(admin.ModelAdmin):
#     list_display = ("name", "code")
#     search_fields = ("name", "code")
#     prepopulated_fields = {"slug": ("name",)}


# @admin.register(State)
# class StateAdmin(admin.ModelAdmin):
#     list_display = ("name", "country")
#     list_filter = ("country",)
#     search_fields = ("name",)
#     prepopulated_fields = {"slug": ("name",)}

# Register your models here.