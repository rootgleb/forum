from django import forms
from .models import Post, Comments, Category
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(attrs={'class': 'dark-theme'}))
    class Meta:
        model = Post
        fields = ('title', 'body', 'category')

    def clean_category(self):
        category = self.cleaned_data['category']
        if category is None:
            raise forms.ValidationError("Пожалуйста, выберите категорию.")
        return category
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
        labels = {'text': '',}
        widgets = {'text': forms.Textarea(attrs={'placeholder': ''}),}



class BanForm(forms.Form):

    days = forms.IntegerField(min_value=0, label='', initial=0, required=True)
    months = forms.IntegerField(min_value=0, label='', initial=0, required=True)
    years = forms.IntegerField(min_value=0, label='', initial=0, required=True)
    hours = forms.IntegerField(min_value=0, label='', initial=0, required=True)
    minutes = forms.IntegerField(min_value=0, label='', initial=0, required=True)
    reason = forms.CharField(max_length=500, label='', widget=forms.Textarea(attrs={'rows': 2}))


