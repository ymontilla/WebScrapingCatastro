# -*- coding: utf-8 -*-
import io
import os
import json
import time

# +
import ijson
import codecs
import warnings

import googlemaps
# -

import pandas as pd

from commons import compute_cross_distances, build_center_point



GOOGLE_MAPS_KEY = os.environ.get('GOOGLE_MAPS_KEY')
gclient = googlemaps.Client(GOOGLE_MAPS_KEY)

# +
"""
Aquí estan listados los tipos de lugares que ahí:

https://developers.google.com/places/supported_types
"""

TYPES = ["accounting", "airport", "amusement_park", "aquarium", "art_gallery",
"atm", "bakery", "bank", "bar", "beauty_salon", "bicycle_store", "book_store",
"bowling_alley", "bus_station", "cafe", "campground", "car_dealer", "car_rental",
"car_repair", "car_wash", "casino", "cemetery", "church", "city_hall",
"clothing_store", "convenience_store", "courthouse", "dentist", "department_store",
"doctor", "drugstore", "electrician", "electronics_store", "embassy", "fire_station",
"florist", "funeral_home", "furniture_store", "gas_station", "gym", "hair_care",
"hardware_store", "hindu_temple", "home_goods_store", "hospital", "insurance_agency",
"jewelry_store", "laundry", "lawyer", "library", "light_rail_station", "liquor_store",
"local_government_office", "locksmith", "lodging", "meal_delivery", "meal_takeaway",
"mosque", "movie_rental", "movie_theater", "moving_company", "museum", "night_club",
"painter", "park", "parking", "pet_store", "pharmacy", "physiotherapist", "plumber",
"police", "post_office", "primary_school", "real_estate_agency", "restaurant",
"roofing_contractor", "rv_park", "school", "secondary_school", "shoe_store", "shopping_mall",
"spa", "stadium", "storage", "store", "subway_station", "supermarket", "synagogue",
"taxi_stand", "tourist_attraction", "train_station", "transit_station", "travel_agency",
"university","veterinary_care", "zoo"]


# -

def dict_to_stream(d):
    sa = json.dumps(d, ensure_ascii=False)
    output = io.StringIO(sa)
    it = ijson.items(output, "results.item")
    return it


def google_nearby_to_df(it):
    if type(it) is dict:
        it = dict_to_stream(it)
    r = []
    for i in it:
        ri = []
        if "locality" in i["types"] or "political" in i["types"]:
            continue
        ri.append(i["name"])
        ri.append(i["geometry"]["location"]["lat"])
        ri.append(i["geometry"]["location"]["lng"])
        for j in TYPES:
            if j in i["types"]:
                ri.append(True)
            else:
                ri.append(False)
        r.append(ri)
    
    z = list(zip(*r))

    if len(z) != 0:
        b = {
            'name': z[0], 
            'lat': z[1], 
            'lon':z[2]
        }
        
        for i in range(len(TYPES)):
            b[TYPES[i]] = z[i + 3]   
    else:
        b = {
            'name': [], 
            'lat': [], 
            'lon': []
        }

        for i in range(len(TYPES)):
            b[TYPES[i]] = []
        
    return pd.DataFrame(b)


def compute_distances(center, places):
    if places.shape[0] == 0:
        return pd.DataFrame(columns=["fid","distance","p_lat","p_lon","i_lat","i_lon","amenity","name"])
    
    places.loc[:, "amenity"] = None
    amenities = ["university", "shopping_mall", "school", "secondary_school", "police", "park", 
             "local_government_office", "library", "hospital", "church", "airport", "amusement_park",
                "bank", "restaurant"]
    condition_amenities = places[amenities[0]]
    places.loc[condition_amenities, "amenity"] = amenities[0]
    for i in range(1, len(amenities)):
        condition_amenity = places[amenities[i]]
        places.loc[condition_amenity, "amenity"] = amenities[i]
        condition_amenities = condition_amenities | condition_amenity
    return compute_cross_distances(center, 
                        places.loc[condition_amenities, ["name", "lat", "lon", "amenity"]])


def query_google_nearby(df, gtype):
    center = build_center_point(df)
    query_result = gclient.places_nearby(
        location=(center.loc[0, "latitude"], center.loc[0, "longitude"]),
        type=gtype,
        rank_by="distance"
    )
    
    results = []
    results.append(compute_distances(center, google_nearby_to_df(query_result)))
    
    while "next_page_token" in query_result:
        time.sleep(5)
        query_result = gclient.places_nearby(page_token=query_result["next_page_token"])
        results.append(compute_distances(center, google_nearby_to_df(query_result)))
    final = pd.concat(results)
    final.index = list(range(final.shape[0]))
    return final.reindex()      
