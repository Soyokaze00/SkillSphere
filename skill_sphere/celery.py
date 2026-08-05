import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skill_sphere.settings.development")

app = Celery("skill_sphere")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
