"""
Development settings for SkillSphere.
"""

import os

from .base import *

DEBUG = True

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-development-key",
)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]
