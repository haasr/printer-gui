from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import never_cache

from .models import *
from .forms import *
from . import settings
from . import file_printer

import os
import re
import random

UPLOADS_DIR = settings.STATICFILES_DIRS[0] + '/uploads/'

# App default settings (color mode, orientation, printer used):
settings = Settings.objects.get(id=1)

@never_cache
def index(request):
    files = File.objects.all()
    context = { 'files': files }
    return render(request, 'index.html', context)


def upload_file(request):
    printer_selected = True

    if request.method != 'POST':
        settings.refresh_from_db()
        if settings.printer_profile == 'None found':
            printer_selected = False

        form = FileUploadForm()
    else:
        fs_storage = FileSystemStorage(location=UPLOADS_DIR)
        upload = request.FILES['file_upload']

        filename = str(random.randint(0, 100)) + re.sub('[^a-zA-Z0-9 \n\.]', '', upload.name)
        filename = filename.replace(' ', '')
        upload.name = filename

        # Get settings object to apply defaults in to the new file object:
        settings.refresh_from_db()

        filename = fs_storage.save(filename, upload)
        new_file = File(
            name=filename,
            page_range='0',
            pages='All',
            color=settings.default_color,
            orientation=settings.default_orientation
        )
        new_file.save()
        return HttpResponseRedirect(reverse('index'))

    context = { 'printer_selected': printer_selected, 'form': form }
    return render(request, 'upload_file.html', context)


def edit_file(request, file_id):
    fileObj = File.objects.get(id=file_id)

    if request.method != 'POST':
        form = FileForm(instance=fileObj)
    else:
        form = FileForm(instance=fileObj, data=request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('index'))

    context = { 'form': form, 'file': fileObj }
    return render(request, 'edit_file.html', context)


def delete_file(request, file_id):
    fileObj = File.objects.get(id=file_id)
    filepath = UPLOADS_DIR + fileObj.name
    fileObj.delete()
    try:
        os.remove(filepath)
    except:
        pass
    return HttpResponseRedirect(reverse('index'))


def print_files(request):
    if request.method == 'POST':
        files = File.objects.all()
        for fileObj in files:
            file_printer.print_file(fileObj.name, fileObj.page_range, fileObj.pages,
                                    fileObj.color, fileObj.orientation)
            fileObj.delete()
    files = File.objects.all()
    context = { 'files': files }
    return render(request, 'index.html', context)


def edit_settings(request):
    settings.refresh_from_db()
    if request.method != 'POST':
        form = SettingsForm(instance=settings)
    else:
        form = SettingsForm(instance=settings, data=request.POST)
        form.save()
        return HttpResponseRedirect(reverse('index'))

    context = { 'settings': settings, 'form': form }
    return render(request, 'settings.html', context)