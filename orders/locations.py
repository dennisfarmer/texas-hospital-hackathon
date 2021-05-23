from django.contrib.gis.geos import Point
from django.db.utils import OperationalError

import pandas as pd
import os
import sys
import requests
import json

# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from .models import Location, Location_Info

datapath = os.path.join(os.path.dirname(__file__), "api_response.json")

def get_locations(refresh=False) -> pd.DataFrame:
    url = "https://api.tchhack.com/locations"
    headers = {"accept": "application/json"}

    if not os.path.exists(datapath) or refresh:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        with open(datapath, "w") as f:
            json.dump(response.json(), f, indent=4)

    locations = pd.read_json(datapath).set_index("id")

    # Only keep a single entry per location, since the only information that
    # matters is the location/latlong
    locations.drop_duplicates(subset=["name"], inplace=True)

    # Fix missing latlong values via manual lookup
    # TODO: Implement Google Maps API call to do this automatically:
    # locations[locations[["latitude", "longitude"]].sum(axis=1) == 0][["address", "city"]]
    locations.loc[
        locations["address"] == "6651 Main Street", ["latitude", "longitude"]
    ] = (29.708410, -95.402610)

    locations.loc[
        locations["address"] == "6330 West Loop South, Suite 300", ["latitude", "longitude"]
    ] = (29.711680, -95.461520)

    return locations


# Read data from .json and insert entries into Location_Info table
def import_locations_to_database(force=False):
    if Location_Info.objects.all().count() > 0:
        if force:
            # DELETE FROM LocationInfo;
            Location_Info.objects.all().delete()
        else:
            print("Database already populated, specify --force to force rewrite")

    if Location_Info.objects.all().count() == 0:
        locations = get_locations()
        for index, row in locations.iterrows():
            info = Location_Info(
                location_id = index,
                name = row["name"],
                address = row["address"],
                city = row["city"],
                state = row["state"],
                zipcode = row["zip"],
                latlong = Point(row["latitude"], row["longitude"]),
                campus = row["campus"],
                photo_url = row["photo"],
                phone = row["phone"])

            info.save()
            Location.objects.filter(location_id=info.location_id).update(info=info)

# Return sequence of two item iterables to use as user selection choices in fields or forms
def get_location_choices():
    try:
        location_choices = [(str(info.pk), info.__str__()) for info in Location_Info.objects.order_by("city")]
    except OperationalError as err:
        print(f"django.db.utils.OperationalError: {err}", "Non-fatal error, continuing...", sep="\n")
        location_choices = [(1, "Location info could not be found")]
    return location_choices


if __name__ == "__main__":
    choice = input("Would you like to print the location choices? [y|N] ")
    if choice.lower() == "y":
        get_location_choices()
    else:
        choice = input("Would you like to overwrite the location database? [y|N] ")
    if choice.lower() == "y":
        import_locations_to_database()

