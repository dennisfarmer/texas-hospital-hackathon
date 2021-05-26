# [Texas Children's Hospital Healthcare Hackathon](https://www.hackerearth.com/challenges/hackathon/texas-childrens-hospital-healthcare-hackathon/)

- Duration: May 14th-24th, 2021
- Project Theme: Food Service and Delivery

South Eats: A Django web application that allows users to create and purchase food orders based on their local eatery and grocery options.


Data links:
- [Generic Food Database](https://data.world/alexandra/generic-food-database)
    - Database of 900 common foods
- [TCH Location Finder API](https://app.swaggerhub.com/apis/Mark-III-Systems/TCH-Locations/1.0.0-oas3#/developers/locations)
    - API that returns all of the Texas Children's locations

## Installation
```zsh
git clone https://github.com/dennisfarmer/texas-hospital-hackathon.git
cd texas-hospital-hackathon

pip install -r requirements.txt
sudo apt-get install -y make libsqlite3-mod-spatialite gdal-bin  # Debian

make fullrefresh
make run
```


## Description

South Eats is a website that aggregates food options from local grocery stores and eatery locations and allow people to order food from them without having to visit the locations or independently research their different options. The idea behind the application is to serve as an easy-to-use interface for a multitude of food delivery services that I don't know how to code. A database is used to store customer orders and order purchases, and the TCH Location Finder API is used to gather the lat-long of each hospital's location to be used in calculating distances from different food stores.

This program is unfortunately pretty bare-bones in terms of features, since I am still in university and don't really know a whole lot yet. There are some features that I wasn't able to implement due to lack of knowledge, such as a multi-selection search box for selecting menu items (if you can get Django's FilteredSelectMultiple widget to work, please let me know! I spent a whole day trying out different approaches/methods and none of them worked on Django 3.2.3) and API interfacing with food stores (aka the actual functionality of the entire application lol).

I want to build upon this project to actually be able to interface with grocery stores and restaurants, and I actually do plan to rebuild the site to be usable in my local area (Michigan) after this campaign has concluded. I don't personally have a use for a hospital food ordering app, but repurposing the web application to be usable for things like pizza orders and food delivery would only take a little bit of API knowledge and would be super doable and creative.
