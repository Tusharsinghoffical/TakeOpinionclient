from django.db import models
from django.utils.text import slugify
from treatments.models import Treatment
from core.models import Country, State


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="hospitals")
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name="hospitals")
    about = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.5)
    is_takeopinion_choice = models.BooleanField(default=False)
    treatments = models.ManyToManyField(Treatment, related_name="hospitals", blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class HospitalMedia(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="media_items")
    image_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return f"Media for {self.hospital.name}"

# Create your models here.
