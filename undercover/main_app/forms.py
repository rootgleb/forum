from django import forms
from .models import Post, Comments, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'category')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
        labels = {'text': '',}
        widgets = {'text': forms.Textarea(attrs={'placeholder': ''}),}



