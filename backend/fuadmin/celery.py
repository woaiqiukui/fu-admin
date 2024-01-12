import os

from celery import Celery, platforms
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "fuadmin.settings")

# app = Celery(f"application")
app = Celery(f"fuadmin")

app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    include=[
            'task.tasks.company',
            'task.tasks.domain',
            'task.tasks.finger',
            'task.tasks.mail',
            'task.tasks.person',
            'task.tasks.poc',
            'task.tasks.port',
            'task.tasks.url',
            ]
)
platforms.C_FORCE_ROOT = True
