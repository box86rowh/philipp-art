"""
WSGI config for philipp_art project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/root/.virtualenvs/philipp-art/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/ec2-user/django-projects/philipp-art')
sys.path.append('/home/ec2-user/django-projects/philipp-art/philipp_art')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "philipp_art.settings.amazon")

# Activate your virtual env
activate_env=os.path.expanduser("root/.virtualenvs/philipp-art/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
