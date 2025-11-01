from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['vet', 'review_text']
        widgets = {
    'review_text': forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 4,
        'placeholder': 'Share your experience with the veterinarian...'
    }),
    'vet': forms.Select(attrs={'class': 'form-select'})
}

