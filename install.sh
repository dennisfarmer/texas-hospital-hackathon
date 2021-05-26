# Installation on Debian WSL:
sudo apt-get install -y python3 libsqlite3-mod-spatialite gdal-bin git make
python -m pip install django pandas numpy django-crispy-forms python-decouple pillow spatialite
git clone https://github.com/dennisfarmer/texas-hospital-hackathon.git
cd texas-hospital-hackathon
make fullrestart

