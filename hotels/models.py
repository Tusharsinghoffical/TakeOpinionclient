from django.db import models
from hospitals.models import Hospital
from django.utils.text import slugify


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    postal_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(default=0)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amenities = models.TextField(blank=True, help_text="Comma-separated list of amenities")
    is_active = models.BooleanField(default=True)
    nearby_hospitals = models.ManyToManyField(Hospital, related_name='nearby_hotels', blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_amenities_list(self):
        """Return amenities as a list"""
        if self.amenities:
            amenities_str = str(self.amenities)
            return [amenity.strip() for amenity in amenities_str.split(',')]
        return []

    class Meta:
        ordering = ['-rating', 'name']
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hotel_images/', blank=True)
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.hotel.name}"

    class Meta:
        ordering = ['-is_primary', 'created_at']
        verbose_name = 'Hotel Image'
        verbose_name_plural = 'Hotel Images'