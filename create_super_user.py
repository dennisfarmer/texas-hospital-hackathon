#!/usr/bin/env python
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "texashospital.settings"
import django
django.setup()
from django.db.utils import IntegrityError

# export DJANGO_SUPERUSER_USERNAME=dennisfarmer
# export DJANGO_SUPERUSER_PASSWORD=securepassword
# export DJANGO_SUPERUSER_EMAIL=admin@djangoproject.com
# python manage.py createsuperuser --noinput

from django.contrib.auth import get_user_model
User = get_user_model()
try:
    User.objects.create_superuser("dennisfarmer", "admin@djangoproject.com", "securepassword")
except IntegrityError as err:
    print("django.db.utils.IntegrityError: ", err, "create_super_user.py: Nonfatal error...", sep="")
    pass
