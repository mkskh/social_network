from django import forms
from .models import Post


class PublishPostForm(forms.ModelForm):
    
    text = forms.Textarea(attrs={'class':'form-control', 'placeholder':''})
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'form-control', 'placeholder':''}))

    class Meta:
        model = Post
        fields = ['text', 'image']
