from django.contrib import admin
from django.utils.html import format_html
from .models import Hotel, HotelImage


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1
    fields = ('image', 'image_url', 'caption', 'is_primary')


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
    list_display = ('hotel', 'is_primary', 'created_at', 'get_image_preview')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('hotel__name', 'caption')
    fields = ('hotel', 'image', 'image_url', 'caption', 'is_primary')
    
    @admin.display(description='Image Preview')
    def get_image_preview(self, obj):
        if obj.get_image_url():
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.get_image_url())
        return "No image"