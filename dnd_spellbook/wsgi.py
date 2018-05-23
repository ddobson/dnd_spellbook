"""
WSGI config for dnd_spellbook project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_file = os.path.join(BASE_DIR, '.env')
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_spellbook.settings")

application = get_wsgi_application()
