#! /bin/bash -
source venv/bin/activate
nohup python3 -u manage.py runserver 192.168.1.133:8000 </dev/null >/dev/null 2>&1 &
