# Django Makefile

MANAGER = python manage.py
DB = ./db.sqlite3

run:
	$(MANAGER) runserver

shell:
	# equivalent to:
	# > export DJANGO_SETTINGS_MODULE=texashospital.settings
	# > ipython
	# > > import django
	# > > django.setup()
	$(MANAGER) shell

refresh:
	rm -f $(DB)
	$(MANAGER) makemigrations
	$(MANAGER) migrate
	$(MANAGER) migrate --run-syncdb
	python import_locations.py

