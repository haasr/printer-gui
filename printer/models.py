from django.db import models


class File(models.Model):
    name = models.CharField(max_length=300)
    page_range = models.CharField(max_length=1, blank=True, null=True)
    pages = models.CharField(max_length=6)
    color = models.CharField(max_length=4)
    orientation = models.CharField(max_length=1)

    class Meta:
        verbose_name_plural = 'files'


class Settings(models.Model):
    app_title = models.CharField(max_length=32, blank=False, null=False)
    default_color = models.CharField(max_length=4, blank=False, null=False)
    default_orientation = models.CharField(max_length=1, blank=False, null=False)
    printer_profile = models.TextField()