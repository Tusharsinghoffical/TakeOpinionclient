from django.db import models
from django.utils.text import slugify


class TreatmentCategory(models.Model):
    TYPE_CHOICES = (
        ("medical", "Medical Treatments"),
        ("aesthetic", "Aesthetic"),
        ("wellness", "Wellness"),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="medical")

    class Meta:
        verbose_name_plural = "Treatment Categories"

    def __str__(self) -> str:
        return f"{self.name} ({self.get_type_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Treatment(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(TreatmentCategory, on_delete=models.CASCADE, related_name="treatments")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# Create your models here.
