from django import forms
from django.db.models import ObjectDoesNotExist
from .models import Homework, Subject

class HomeworkForm(forms.Form):
    subject_id = forms.IntegerField(widget=forms.HiddenInput)
    file = forms.FileField(label='上傳檔案')

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(HomeworkForm, self).__init__(*args, **kwargs)

    def clean(self):
        #if user authenticated
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用戶尚未登入')
            
        subject_id = self.cleaned_data['subject_id']
        try:
            model_subject = Subject.objects.get(pk=subject_id)
            self.cleaned_data['subject'] = model_subject
        except ObjectDoesNotExist:
            raise forms.ValidationError('作業不存在')
        return self.cleaned_data

