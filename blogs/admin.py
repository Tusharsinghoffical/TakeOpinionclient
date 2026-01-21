from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "published_at", "is_medical_visa")
    list_filter = ("is_medical_visa",)

# Register your models here.
