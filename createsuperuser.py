#!/usr/bin/env python
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "texashospital.settings"
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser("dennisfarmer", "admin@django.url", "securepassword")
