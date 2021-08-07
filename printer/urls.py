"""printer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
