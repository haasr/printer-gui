import os
import re
from . import settings
from .models import Settings

UPLOADS_DIR = settings.STATICFILES_DIRS[0] + '/uploads/'
CONVERTED_DIR = settings.STATICFILES_DIRS[0] + '/converted_uploads/'

settings = Settings.objects.get(id=1)

# requires cups, pandoc, and texlive-latex-extra be installated

def print_file(filename, page_range, pages, color, orientation):
    settings.refresh_from_db()
    printer = settings.printer_profile

    if filename.endswith('.docx'):
        copy_filename = filename.rstrip('.docx') + '.pdf'
        os.system('pandoc -o ' + CONVERTED_DIR + copy_filename
                    + ' -f docx ' + UPLOADS_DIR + filename)

        if page_range == '0':
            command = ('lp -d ' + printer + ' -o orientation-requested=' + orientation +
                        ' -o ColorModel=' + color + ' ' + CONVERTED_DIR + copy_filename)
        else:
            command = ('lp -d ' + printer + ' -P ' + pages + ' -o ' + ' orientation-requested=' + orientation +
                        ' -o ColorModel=' + color + ' ' + CONVERTED_DIR + copy_filename)
        os.system(command)
        os.system('rm ' + CONVERTED_DIR + copy_filename)
    else:
        if page_range == '0':
            command = ('lp -d ' + printer + ' -o orientation-requested=' + orientation +
                        ' -o ColorModel=' + color + ' ' + UPLOADS_DIR + filename)
        else:
            command = ('lp -d ' + printer + ' -P ' + pages + ' -o ' + ' orientation-requested=' + orientation +
                        ' -o ColorModel=' + color + ' ' + UPLOADS_DIR + filename)
        os.system(command)

    os.system('rm ' + UPLOADS_DIR + filename)