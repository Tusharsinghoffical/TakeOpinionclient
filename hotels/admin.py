from django.contrib import admin
from .models import Hotel, HotelImage


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'rating', 'is_active', 'created_at')
    list_filter = ('is_active', 'city', 'state', 'rating', 'created_at')
    search_fields = ('name', 'city', 'state', 'address')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [HotelImageInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('hotel__name', 'caption')