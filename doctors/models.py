from django.db import models
from django.utils.text import slugify
from treatments.models import Treatment
from hospitals.models import Hospital


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    key_points = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    treatments = models.ManyToManyField(Treatment, related_name="doctors", blank=True)
    hospitals = models.ManyToManyField(Hospital, related_name="doctors", blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# Create your models here.
