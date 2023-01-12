from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('edit_file/<int:file_id>/', views.edit_file, name='edit_file'),
    path('submit_edit_file_form/', views.submit_edit_file_form, name='submit_edit_file_form'),
    path('delete_file<int:file_id>/', views.delete_file, name='delete_file'),
    path('print_files/', views.print_files, name='print_files'),
    path('settings', views.edit_settings, name='settings'),
]
