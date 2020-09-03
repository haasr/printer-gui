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


@never_cache
def index(request):
    files = File.objects.all()
    context = { 'files': files }
    return render(request, 'index.html', context)


def upload_file(request):
    if request.method != 'POST':
        form = FileUploadForm()
    else:
        fs_storage = FileSystemStorage(location=UPLOADS_DIR)
        upload = request.FILES['file_upload']

        filename = str(random.randint(0, 100)) + re.sub('[^a-zA-Z0-9 \n\.]', '', upload.name)
        filename = filename.replace(' ', '')
        upload.name = filename

        filename = fs_storage.save(filename, upload)
        new_file = File(
            name=filename,
            page_range='0',
            pages='All',
            color='RGB',
            orientation='3'
        )
        new_file.save()
        return HttpResponseRedirect(reverse('index'))

    context = { 'form': form }
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
            print('Send to File Printer')
            print(fileObj.color)
            file_printer.print_file(fileObj.name, fileObj.page_range, fileObj.pages,
                                    fileObj.color, fileObj.orientation)
            print('Delete object')
            fileObj.delete()
    files = File.objects.all()
    context = { 'files': files }
    return render(request, 'index.html', context)
