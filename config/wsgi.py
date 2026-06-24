# -*- coding: utf-8 -*-
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
# Vercel (@vercel/python) busca una variable WSGI llamada `app`.
app = application
