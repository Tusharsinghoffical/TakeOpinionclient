from django import forms
from .models import DoctorMedia


class DoctorMediaForm(forms.ModelForm):
    class Meta:
        model = DoctorMedia
        fields = ['image_url']
        widgets = {
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter image URL'}),
        }