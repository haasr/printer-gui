#! /bin/bash -

cd /home/pi/printer-gui
source venv/bin/activate
python3 manage.py runserver 192.168.1.133:8000