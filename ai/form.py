from django import forms

from .models import File

class FileFieldForm(forms.Form):
    filefield = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple":True}))