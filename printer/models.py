from django.db import models
from . import settings

import os


UPLOADS_DIR = settings.STATICFILES_DIRS[0] + '/uploads/'
CONVERTED_DIR = settings.STATICFILES_DIRS[0] + '/converted_uploads/'


class File(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=300)
    page_range = models.CharField(max_length=1, blank=True, null=True)
    pages = models.CharField(max_length=6)
    color = models.CharField(max_length=4)
    orientation = models.CharField(max_length=1)
    file_type = models.CharField(max_length=20)

    def determine_file_type(self, filename):
        if filename.endswith('pdf'):
            self.file_type = 'PDF'
        elif filename.endswith('doc'):
            self.file_type = 'Word (2003)'
        elif filename.endswith('docx'):
            self.file_type = 'Word (2007)'
        elif filename.endswith('odt'):
            self.file_type = 'OpenDocument Text'
        elif filename.endswith('rtf'):
            self.file_type = 'Rich Text Format'
        else:
            self.file_type = 'Unknown format'

    def save(self, *args, **kwargs):
        self.determine_file_type(self.name.lower())

        super(File, self).save(*args, **kwargs)

    def delete(self):
        # Delete the physical file (included pdf conversion), if existing
        try:
            os.remove(f"{UPLOADS_DIR}{self.name}")
            os.remove(f"{CONVERTED_DIR}{os.path.splitext(self.name)[1]}.pdf")
        except:
            pass

        super(File, self).delete()

    class Meta:
        verbose_name_plural = 'files'


class Settings(models.Model):
    app_title = models.CharField(max_length=32, blank=False, null=False)
    default_color = models.CharField(max_length=4, blank=False, null=False)
    default_orientation = models.CharField(max_length=1, blank=False, null=False)
    printer_profile = models.TextField()