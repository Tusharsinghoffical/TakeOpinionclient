from django.db import models
from django.utils.text import slugify
from treatments.models import Treatment
from core.models import Country, State
from core.validators import validate_image_url


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="hospitals")
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name="hospitals")
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    about = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.5)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    is_takeopinion_choice = models.BooleanField(default=False)
    treatments = models.ManyToManyField(Treatment, related_name="hospitals", blank=True)
    
    # Contact information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    
    # Hospital details
    established_year = models.PositiveIntegerField(null=True, blank=True)
    beds_count = models.PositiveIntegerField(null=True, blank=True)
    staff_count = models.PositiveIntegerField(null=True, blank=True)
    departments_count = models.PositiveIntegerField(null=True, blank=True)
    awards_count = models.PositiveIntegerField(null=True, blank=True)
    
    # Certifications
    jci_accredited = models.BooleanField(default=False)
    nabh_accredited = models.BooleanField(default=False)
    iso_certified = models.BooleanField(default=False)
    
    # Profile picture
    profile_picture = models.URLField(blank=True, help_text="URL to hospital's profile/thumbnail picture", validators=[validate_image_url])

    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class HospitalMedia(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="media_items")
    image_url = models.URLField(blank=True, validators=[validate_image_url])

    def __str__(self) -> str:
        return f"Media for {self.hospital.name}"

# Create your models here.