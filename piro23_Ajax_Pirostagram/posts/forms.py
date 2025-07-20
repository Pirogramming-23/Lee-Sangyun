from django import forms
from .models import Post, Story
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image']
        
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)