import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/.virtualenvs/philipp-art/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/ubuntu/django/philipp-art/philipp_art')
sys.path.append('/home/ubuntu/django/philipp-art/philipp_art/philipp_art')

os.environ['DJANGO_SETTINGS_MODULE'] = 'philipp_art.settings.amazon'

# Activate your virtual env
activate_env=os.path.expanduser("/home/ubuntu/.virtualenvs/philipp-art/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()