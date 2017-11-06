from django import forms
from .models import Comment,Somt


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']


class SomtForm(forms.ModelForm):
    class Meta:
        model = Somt
        fields = ['name', 'email']