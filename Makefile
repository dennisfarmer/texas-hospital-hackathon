# Django Makefile

MANAGER = python manage.py
DB = ./db.sqlite3

run:
	$(MANAGER) runserver

# Start the django python shell to test model imports, equivalent to:
# > export DJANGO_SETTINGS_MODULE=texashospital.settings
# > ipython
# > > import django
# > > django.setup()
shell:
	$(MANAGER) shell

# Migrate the database model to sqlite database and populate
# the Location_Info table with values
refresh:
	$(MANAGER) makemigrations
	$(MANAGER) migrate
	$(MANAGER) migrate --run-syncdb
	python import_locations.py $(args)

# Create a user that can be used to access django's admin page
createsuperuser:
	export DJANGO_SUPERUSER_USERNAME=dennisfarmer
	export DJANGO_SUPERUSER_PASSWORD=securepassword
	export DJANGO_SUPERUSER_EMAIL=admin@djangoproject.com
	$(MANAGER) createsuperuser --noinput

# Perform a migration on the database model and start the server
restart:
	make refresh
	make run

# Drop all tables and recreate the database, then start the server
fullrestart:
	rm -f $(DB)
	make refresh args="--force"
	make createsuperuser
	make run

