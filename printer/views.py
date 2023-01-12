from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import never_cache

from .models import *
from .forms import *
from . import settings
from . import file_printer

import re


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

        filename = re.sub('[^a-zA-Z0-9.]', '-', upload.name)
        upload.name = filename

        # Get settings object to apply defaults to the new file object:

        filename = fs_storage.save(filename, upload)
        new_file = File(
            name=upload.name, page_range='0', pages='All',
            color=settings.default_color,
            orientation=settings.default_orientation
        )
        new_file.save()
        return HttpResponseRedirect(reverse('index'))

    context = { 'printer_selected': printer_selected, 'form': form }
    return render(request, 'upload_file.html', context)


def edit_file(request, file_id):
    fileObj = File.objects.get(id=file_id)
    fileObj.refresh_from_db()
    context = { 'file': fileObj }
    return render(request, 'edit_file.html', context)


def submit_edit_file_form(request):
    if request.method == 'POST':
        fileObj = File.objects.get(id=int(request.POST['file_id']))
        fileObj.name = request.POST['name']
        fileObj.page_range = request.POST['page_range']
        fileObj.pages = request.POST['pages']
        fileObj.color = request.POST['color']
        fileObj.orientation = request.POST['orientation']
        fileObj.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def delete_file(request, file_id):
    fileObj = File.objects.get(id=file_id)
    fileObj.delete()
    
    return HttpResponseRedirect(reverse('index'))


def print_files(request):
    if request.method == 'POST':
        files = File.objects.all()
        
        errors = False
        for fileObj in files:
            output = file_printer.print_file(fileObj.name, fileObj.page_range,
                                fileObj.pages, fileObj.color, fileObj.orientation)
            err = output[1].decode()
            if err != '':
                errors = True
                messages.error(request, err)
            else:
                messages.info(request, f"Printing {fileObj.name}")
            
            fileObj.delete()

        if errors:
            return HttpResponse(status=500)
        else:
            messages.success(request, 'Jobs completed')
            return HttpResponse(status=204) # OK, Nothing to return
    return HttpResponse(status=403) # !POST forbidden


def edit_settings(request):
    settings.refresh_from_db()
    if request.method != 'POST':
        form = SettingsForm(instance=settings)
    else:
        form = SettingsForm(instance=settings, data=request.POST)
        form.save()
        file_printer.refresh_printer_profile()
        return HttpResponseRedirect(reverse('index'))

    context = { 'settings': settings, 'form': form }
    return render(request, 'settings.html', context)