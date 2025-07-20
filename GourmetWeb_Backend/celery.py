from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establecer configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GourmetWeb_Backend.settings')

app = Celery('GourmetWeb_Backend')

# Configuración usando settings de Django con prefijo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover de tareas
app.autodiscover_tasks()
