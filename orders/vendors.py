from numpy.random import ranf
from numpy import sqrt

vendors = ["H.E.B.", "Whole Foods", "Kroger"]

city_locations = {'The Woodlands': (30.1658, -95.4613), 'Austin':(30.2672, -97.7431), 'Houston':(29.7604, -95.3698), 'Kingwood':(30.0500, -95.1845), 'Humble':(29.9988, -95.2622), 'Bellaire':(29.7058, -95.4588), 'Cypress':(29.9717, -95.6938), 'Pearland':(29.5636, -95.2860), 'Katy':(29.7858, -95.8245), 'McAllen':(26.2034, -98.2300), 'Sugar Land':(29.5984, -95.6226), 'Webster':(29.5377, -95.1183)}

#city_locations = {k.lower(): v for k, v in city_locations.items()}


# for testing purposes, generate random (lat, long)
def rand_loc(latlong: "(lat, long)"):
    return [dim[0] - dim[1] for dim in zip(latlong, [n-0.5 for n in ranf(size=2)])]

def delta_distance_miles(a, b):
        # rough parameter that averages lat->mi and long->mi, more accurate estimates would use trig
        miles_per_latlong = 64
        delta_lat = a[0] - b[0]
        delta_long = a[1] - b[1]
        return sqrt(delta_lat**2 + delta_long**2) * miles_per_latlong

def get_vendors_in(city, latlong):
    L = []
    for v in vendors:
        v_loc = rand_loc(city_locations[city])
        delta_d = round(delta_distance_miles(v_loc, latlong), 2)
        L.append((f"{v}, {v_loc[0]}, {v_loc[1]}, {delta_d}", f"{v} - {delta_d} miles away"))
    return [([v,city,rand_loc(city_locations[city])] , f"{v} - {city}: ") for v in vendors]


# TODO: implement inventory system (that's like a bunch of work so no lol)

