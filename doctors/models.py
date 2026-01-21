from django.db import models
from django.utils.text import slugify
from treatments.models import Treatment
from hospitals.models import Hospital
from core.validators import validate_image_url, validate_youtube_url


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    key_points = models.TextField(blank=True)
    about = models.TextField(blank=True, help_text="Detailed description of the doctor's background and expertise")
    education = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)  # type: ignore
    treatments = models.ManyToManyField(Treatment, related_name="doctors", blank=True)
    hospitals = models.ManyToManyField(Hospital, related_name="doctors", blank=True)
    awards = models.TextField(blank=True, help_text="Enter awards separated by new lines")
    
    # Contact information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    
    # Rating information
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    review_count = models.PositiveIntegerField(default=0)  # type: ignore
    
    # Professional details
    medical_license_number = models.CharField(max_length=50, blank=True)
    languages_spoken = models.CharField(max_length=200, blank=True, help_text="Languages spoken by the doctor, separated by commas")
    
    # Profile picture
    profile_picture = models.URLField(blank=True, help_text="URL to doctor's profile picture", validators=[validate_image_url])

    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_treatment_price_at_hospital(self, treatment_id: int, hospital_id: int) -> float | None:
        """
        Get the price for a specific treatment at a specific hospital where this doctor practices
        """
        try:
            # Check if doctor practices at the specified hospital
            if not self.hospitals.filter(id=hospital_id).exists():  # type: ignore
                return None
                
            # Check if doctor offers the specified treatment
            if not self.treatments.filter(id=treatment_id).exists():  # type: ignore
                return None
                
            # Get the hospital's pricing for this treatment
            hospital = Hospital.objects.get(id=hospital_id)  # type: ignore
            treatment = Treatment.objects.get(id=treatment_id)  # type: ignore
            
            # Return the hospital's starting price for this treatment
            return float(hospital.starting_price)
        except (Hospital.DoesNotExist, Treatment.DoesNotExist):  # type: ignore
            return None


class DoctorMedia(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="media_items")
    image_url = models.URLField(blank=True, validators=[validate_image_url])
    video_url = models.URLField(blank=True, validators=[validate_youtube_url])  # Re-adding video URL support

    def __str__(self) -> str:
        return f"Media for {self.doctor.name}"

    @property
    def is_video(self) -> bool:
        return bool(self.video_url)

    @property
    def is_image(self) -> bool:
        return bool(self.image_url)

# Create your models here.