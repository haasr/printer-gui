from django import forms
from .models import *
import subprocess

# Get available printer profiles:
available_printer_profiles = [] # List of tuples for available printer profiles
try:
    proc = subprocess.Popen(['lpstat', '-a'], shell=False,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    stdout = proc.communicate()[0].decode('utf-8')
    stdout_list = stdout.split('\n')
    list_len = len(stdout_list)
    stdout_list.remove(stdout_list[(list_len - 1)]) # Remove blank element at end.

    for i in range(0, (list_len - 1)):
        stdout_list[i] = stdout_list[i].split(' accepting')[0]

    for profile in stdout_list:
        available_printer_profiles.append((profile, profile))
except:
    available_printer_profiles.append(('None found', 'None found'))


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


class SettingsForm(forms.ModelForm):
    app_title = forms.CharField(
        label = 'App title',
    )
    default_color = forms.CharField(
        label='Color default',
        widget=forms.Select(
            choices=PrintOptions.COLOR_OPTIONS
        )
    )
    default_orientation = forms.CharField(
        label='Orientation default',
        widget=forms.Select(
            choices=PrintOptions.ORIENTATION_OPTIONS
        )
    )
    printer_profile = forms.CharField(
        label='Printer Profile',
        widget=forms.Select(
            choices=available_printer_profiles
        )
    )

    class Meta:
        model = Settings
        fields = [ 'app_title', 'default_color', 'default_orientation',
                    'printer_profile' ]

