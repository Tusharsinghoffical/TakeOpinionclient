from django import forms
from .models import DoctorMedia


class DoctorMediaForm(forms.ModelForm):
    class Meta:
        model = DoctorMedia
        fields = ['image_url', 'video_url']
        widgets = {
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter image URL'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter YouTube video URL (optional)'}),
        }
        
    def clean_image_url(self):
        image_url = self.cleaned_data.get('image_url')
        if image_url:
            # Basic validation for image URLs
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']
            if not any(image_url.lower().endswith(ext) for ext in image_extensions):
                raise forms.ValidationError("Please provide a valid image URL (jpg, jpeg, png, gif, webp, bmp, svg).")
        return image_url
        
    def clean_video_url(self):
        video_url = self.cleaned_data.get('video_url')
        if video_url:
            # Basic validation for YouTube URLs
            youtube_domains = ['youtube.com', 'youtu.be']
            if not any(domain in video_url.lower() for domain in youtube_domains):
                raise forms.ValidationError("Please provide a valid YouTube video URL.")
        return video_url