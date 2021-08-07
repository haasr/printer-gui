import os
import subprocess
from . import settings
from .models import Settings

UPLOADS_DIR = settings.STATICFILES_DIRS[0] + '/uploads/'
CONVERTED_DIR = settings.STATICFILES_DIRS[0] + '/converted_uploads/'

settings = Settings.objects.get(id=1)
printer = settings.printer_profile
# requires cups, pandoc, and texlive-latex-extra be installated

def refresh_printer_profile():
    global printer
    settings.refresh_from_db()
    printer = settings.printer_profile


def print_file(filename, page_range, pages, color, orientation):
    global printer

    if filename.endswith('.docx'):
        copy_filename = filename.rstrip('.docx') + '.pdf'
        command = [
            'pandoc', '-o', (CONVERTED_DIR + copy_filename), '-f',
            'docx', (UPLOADS_DIR + filename)
        ]
        conv_proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        conv_proc.wait()

        if page_range == '0':
            command = [
                'lp', '-d', printer, '-o', ('orientation-requested=' + orientation),
                '-o', ('ColorModel=' + color ), (CONVERTED_DIR + copy_filename)
            ]
        else:
            command = [
                'lp', '-d', printer, '-P', pages, '-o', 
                ('orientation-requested=' + orientation), '-o',
                ('ColorModel=' + color), (CONVERTED_DIR + copy_filename)
            ]
        print_proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        print_proc.wait()
        os.system(f"rm {CONVERTED_DIR}{copy_filename}")
    else:
        if page_range == '0':
            command = [
                'lp', '-d', printer, '-o', ('orientation-requested=' + orientation),
                '-o', ('ColorModel=' + color), (UPLOADS_DIR + filename)
            ]
        else:
            command = [
                'lp', '-d', printer, '-P', pages, '-o',
                ('orientation-requested=' + orientation), '-o', ('ColorModel=' + color),
                (UPLOADS_DIR + filename)
            ]
        print_proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        print_proc.wait()

    os.system(f"rm {UPLOADS_DIR}{filename}")