# skillsphere/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill_sphere.settings')
app = Celery('skill_sphere')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
