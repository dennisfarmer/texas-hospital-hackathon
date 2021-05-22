#!/usr/bin/env python
import os
import argparse
os.environ["DJANGO_SETTINGS_MODULE"] = "texashospital.settings"
import django
django.setup()

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--force", help="if location_info database contains entries, drop the entries and repopulate instead of exiting", action="store_true")
args = parser.parse_args()

from orders.locations import import_locations_to_database
import_locations_to_database(force=args.force)

