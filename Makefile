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
	python write_to_db.py $(args)

# Perform a migration on the database model and start the server
restart:
	make refresh
	make run

# Drop all tables and recreate the database, then start the server
fullrestart:
	rm -f $(DB)
	make refresh args="--force"
	python create_super_user.py
	make run

