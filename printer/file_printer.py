import os
import re
from . import settings

UPLOADS_DIR = settings.STATICFILES_DIRS[0] + '/uploads/'
CONVERTED_DIR = settings.STATICFILES_DIRS[0] + '/converted_uploads/'


# requires cups, pandoc, and texlive-latex-extra be installated

def print_file(filename, page_range, pages, color, orientation):
    print ('PRINTING  ' + filename)

    if filename.endswith('.docx'):
        copy_filename = filename.rstrip('.docx') + '.pdf'
        os.system('pandoc -o ' + CONVERTED_DIR + copy_filename
                    + ' -f docx ' + UPLOADS_DIR + filename)

        if re.match(r'[0-9]-[0-9].*', page_range):
            print('PRINT RANGE ' + page_range)
            command = ('lp -d EPSON_XP_310_Series -P ' + page_range + ' -o ' + ' orientation-requested=' + orientation +
                        ' -o ColorModel=' + color + ' ' + CONVERTED_DIR + copy_filename)
        else:
            print('ALL PAGES')
            command = ('lp -d EPSON_XP_310_Series -o orientation-requested=' + orientation +
                        ' -o ColorModel=' + color + ' ' + CONVERTED_DIR + copy_filename)
            
        print(command)
        os.system(command)
        os.system('rm ' + CONVERTED_DIR + copy_filename)
    else:
        if re.match(r'[0-9]-[0-9].*', page_range):
            print('PRINT RANGE ' + page_range)
            command = ('lp -d EPSON_XP_310_Series -P ' + page_range + ' -o ' + ' orientation-requested=' + orientation +
                        ' -o ColorModel=' + color + ' ' + UPLOADS_DIR + filename)
        else:
            command = ('lp -d EPSON_XP_310_Series -o orientation-requested=' + orientation +
                        ' -o ColorModel=' + color + ' ' + UPLOADS_DIR + filename)
            print('ALL PAGES')
        print(command)
        os.system(command)

    os.system('rm ' + UPLOADS_DIR + filename)