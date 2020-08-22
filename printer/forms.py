from django import forms
from .models import *

class PrintOptions:
    RANGE_OPTIONS = (
        ('0', 'All pages'),
        ('1', 'Custom range') 
    )
    COLOR_OPTIONS = (
        ('Gray', 'Grayscale'),
        ('RGB', 'Color')
    )
    ORIENTATION_OPTIONS = (
        ('3', 'Portrait'),
        ('4', 'Landscape')
    )


class FileUploadForm(forms.Form):
    file_upload = forms.FileField(
        label='Upload PDF or DOCX',
        required=True,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        })
    )


class FileForm(forms.ModelForm):
    name = forms.CharField(
        label='Filename',
        disabled=True,
    )
    page_range = forms.CharField(
        label='Page Range',
        widget=forms.Select(
            choices=PrintOptions.RANGE_OPTIONS
        )
    )
    pages = forms.CharField(
        label='Range (If Custom)',
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. 1-4'
        })
    )
    color = forms.CharField(
        label='Color',
        widget=forms.Select(
            choices=PrintOptions.COLOR_OPTIONS
        )
    )
    orientation = forms.CharField(
        label='Orientation',
        widget=forms.Select(
            choices=PrintOptions.ORIENTATION_OPTIONS
        )
    )

    class Meta:
        model = File
        fields = [ 'name', 'page_range', 'pages', 'color', 'orientation' ]