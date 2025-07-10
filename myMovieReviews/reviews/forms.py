from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'title', 'release_year', 'genre', 'rating', 
            'running_time', 'content', 'director', 'actors'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0', 'max': '5'}),
            'running_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'actors': forms.TextInput(attrs={'class': 'form-control'}),
        }