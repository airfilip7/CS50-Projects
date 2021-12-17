from django import forms
from .models import *

class AddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
    
    content = forms.CharField(max_length=4096, widget=forms.Textarea(attrs={'placeholder': "Write a comment...", 'class': 'form-control'}))
