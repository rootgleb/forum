from django import forms
from .models import Post, Comments


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', "category")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

