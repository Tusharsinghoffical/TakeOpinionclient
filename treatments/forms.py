from django import forms


class TreatmentMediaForm(forms.Form):
    image_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter image URL'}),
        help_text="Enter a valid image URL (jpg, jpeg, png, gif, webp, bmp, svg)"
    )
    
    def clean_image_url(self):
        image_url = self.cleaned_data.get('image_url')
        if image_url:
            # Basic validation for image URLs
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']
            if not any(image_url.lower().endswith(ext) for ext in image_extensions):
                raise forms.ValidationError("Please provide a valid image URL (jpg, jpeg, png, gif, webp, bmp, svg).")
        return image_url