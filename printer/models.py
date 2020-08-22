from django.db import models


class File(models.Model):
    name = models.CharField(max_length=300)
    page_range = models.CharField(max_length=1, blank=True, null=True)
    pages = models.CharField(max_length=6)
    color = models.CharField(max_length=4)
    orientation = models.CharField(max_length=1)

    class Meta:
        verbose_name_plural = 'files'