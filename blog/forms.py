from django import forms
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Blog, BlogType

class BlogForm(forms.Form):
    title = forms.CharField(
        label='文章標題', 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'請輸入標題'}
        )
    )
    blog_type = forms.ModelChoiceField(
        label='文章分類',
        queryset=BlogType.objects.all(),
        to_field_name="type_name",
        widget=forms.Select(
            attrs={'class':'form-control', 'placeholder':'請選擇分類', 'id': 'blog_type'}
        )
    )
    content = forms.CharField(
        label='內文',
        widget=CKEditorWidget(config_name='blog_ckeditor')
    )
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(BlogForm, self).__init__(*args, **kwargs)

    def clean(self):
        #if user authenticated
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用戶尚未登入')
        return self.cleaned_data