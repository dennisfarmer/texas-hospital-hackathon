#!/usr/bin/env python
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "texashospital.settings"
import django
django.setup()

# export DJANGO_SUPERUSER_USERNAME=dennisfarmer
# export DJANGO_SUPERUSER_PASSWORD=securepassword
# export DJANGO_SUPERUSER_EMAIL=admin@djangoproject.com
# python manage.py createsuperuser --noinput

from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser("dennisfarmer", "admin@djangoproject.com", "securepassword")
