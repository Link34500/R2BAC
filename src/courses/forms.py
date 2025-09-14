from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
  content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Ajouter un commentaire...'}),min_length=2,max_length=2000, required=True)
  class Meta:
    model = Comment
    fields = ['content','parent']