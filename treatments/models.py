from django.db import models
from django.utils.text import slugify
from typing import List


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
        # This is a Django auto-generated method, safe to ignore linter warning
        return f"{self.name} ({self.get_type_display()})"  # type: ignore

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Treatment(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(TreatmentCategory, on_delete=models.CASCADE, related_name="treatments")
    
    # Additional fields used in templates
    duration = models.CharField(max_length=100, blank=True, default="5-7 days")
    anesthesia_type = models.CharField(max_length=100, blank=True, default="General")
    recovery_time = models.CharField(max_length=100, blank=True, default="2-3 weeks")
    procedure_details = models.TextField(blank=True, default="This treatment involves a comprehensive approach to address your medical condition with the latest techniques and technology. The procedure is performed by highly qualified specialists in state-of-the-art facilities.")
    preparation_guidelines = models.TextField(blank=True, default="Consult your doctor,Stop certain medications,Complete medical tests,Fast before procedure")
    aftercare_instructions = models.TextField(blank=True, default="Rest and recovery period,Medication schedule,Follow-up appointments,Activity restrictions")
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    review_count = models.PositiveIntegerField(default=120)  # type: ignore

    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_preparation_guidelines(self) -> List[str]:
        """Return preparation guidelines as a list"""
        if self.preparation_guidelines:
            return str(self.preparation_guidelines).split(',')
        return []

    def get_aftercare_instructions(self) -> List[str]:
        """Return aftercare instructions as a list"""
        if self.aftercare_instructions:
            return str(self.aftercare_instructions).split(',')
        return []


class TreatmentFAQ(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)  # type: ignore

    class Meta:
        ordering = ['order']
        verbose_name = "Treatment FAQ"
        verbose_name_plural = "Treatment FAQs"

    def __str__(self) -> str:
        return f"FAQ for {self.treatment.name}: {self.question}"

# Create your models here.