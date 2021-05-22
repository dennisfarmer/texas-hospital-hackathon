#!/usr/bin/env python
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "texashospital.settings"
import django
django.setup()
from orders.locations import import_locations_to_database
import_locations_to_database(overwrite=True)

