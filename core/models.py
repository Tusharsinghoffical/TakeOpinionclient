from django.db import models
from django.utils.text import slugify


class Country(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=2, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    flag_url = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.flag_url:
            self.flag_url = f"https://flagcdn.com/w40/{self.code.lower()}.png"
        super().save(*args, **kwargs)


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states")
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=10, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = ("country", "name")
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}, {self.country.code}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.country.code}-{self.name}")
        super().save(*args, **kwargs)

# Create your models here.
