pip install django pandas django-annoying django-crispy-forms python-decouple pillow django-select2
sudo apt-get install -y libsqlite3-mod-spatialite gdal-bin


# Deployment using Heroku
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
# (5:19)

# caching for select-2
sudo apt-get install -y redis-server
# or?
# pip install django-redis

# also
sudo apt-get install -y libjs-jquery

#start cache server:
redis-server

# python -m pip install ...
