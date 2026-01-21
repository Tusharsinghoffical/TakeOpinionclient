from django import forms
from .models import HospitalMedia


class HospitalMediaForm(forms.ModelForm):
    class Meta:
        model = HospitalMedia
        fields = ['image_url']
        widgets = {
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter image URL'}),
        }
        
    def clean_image_url(self):
        image_url = self.cleaned_data.get('image_url')
        if image_url:
            # Basic validation for image URLs
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']
            if not any(image_url.lower().endswith(ext) for ext in image_extensions):
                raise forms.ValidationError("Please provide a valid image URL (jpg, jpeg, png, gif, webp, bmp, svg).")
        return image_url