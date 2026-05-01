from django.db import models
from hospitals.models import Hospital
from django.utils.text import slugify
from datetime import date
from django.core.exceptions import ValidationError
from typing import Optional


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
    review_count = models.PositiveIntegerField(default=0)  # type: ignore
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amenities = models.TextField(blank=True, help_text="Comma-separated list of amenities")
    is_active = models.BooleanField(default=True)  # type: ignore
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
    image = models.ImageField(upload_to='hotel_images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="Enter an image URL instead of uploading a file")
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.image:
            return f"Image for {self.hotel.name}"
        elif self.image_url:
            return f"Image URL for {self.hotel.name}"
        else:
            return f"Image for {self.hotel.name} (no image)"

    def get_image_url(self) -> Optional[str]:
        """Return the image URL, preferring uploaded image over URL field"""
        # Check if we have an uploaded image and it has a file associated
        if self.image and hasattr(self.image, 'url'):
            try:
                # This will raise ValueError if no file is associated
                return self.image.url  # type: ignore
            except ValueError:
                # No file associated with the image field
                pass
        
        # Fall back to image_url field
        if self.image_url:
            return str(self.image_url)  # Convert to string to satisfy type checker
            
        # No image available
        return None

    def clean(self) -> None:
        """Validate that either image or image_url is provided, but not both"""
        if self.image and self.image_url:
            raise ValidationError("Please provide either an uploaded image or an image URL, not both.")
        if not self.image and not self.image_url:
            raise ValidationError("Please provide either an uploaded image or an image URL.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-is_primary', 'created_at']  # type: ignore
        verbose_name = 'Hotel Image'
        verbose_name_plural = 'Hotel Images'


class HotelBooking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=200)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField(default=1)  # type: ignore
    number_of_rooms = models.PositiveIntegerField(default=1)  # type: ignore
    special_requests = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    booking_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking for {self.hotel.name} by {self.guest_name}"

    def get_nights_count(self) -> int:
        """Calculate the number of nights"""
        if self.check_in_date and self.check_out_date:
            # type: ignore
            delta = self.check_out_date - self.check_in_date  # type: ignore
            return delta.days
        return 0

    def save(self, *args, **kwargs):
        # Calculate total amount if not set
        if not self.total_amount and hasattr(self, 'hotel') and getattr(self.hotel, 'price_per_night', None):
            nights = self.get_nights_count()
            price_per_night = float(str(self.hotel.price_per_night))  # type: ignore
            num_rooms = int(self.number_of_rooms)  # type: ignore
            self.total_amount = price_per_night * float(nights) * float(num_rooms)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Hotel Booking'
        verbose_name_plural = 'Hotel Bookings'