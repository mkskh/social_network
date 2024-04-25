from django import forms
from .models import Post


class PublishPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What would you like to share today?'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }