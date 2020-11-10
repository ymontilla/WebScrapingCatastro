# -*- coding: utf-8 -*-
import io
import json

import pandas as pd

import ijson
import codecs
import warnings

from commons import read_csv_with_encoding, read_json_with_encoding, distance



TRANSMILENIO_FILENAME = "bogota/transmilenio"
BOGOTA_INTEREST_POINTS = "bogota/bogota_interest_points.json"

def nearestBusStop(point, transmilenio):
    d = 99999999
    n = ""
    for i in trasmilenio:
        p = distance(point["latitude"], point["longitude"], transmilenio[i]["lat"], transmilenio[i]["lon"])
        if p < d:
            d = p
            n = transmilenio[i]["name"]
    return n

def read_transmilenios_as_df():
    a = read_json_with_encoding(TRANSMILENIO_FILENAME)
    to_array = lambda e: [e["lat"], e["lon"], e["name"]]
    b = list(zip(*map(to_array, a.values())))
    return pd.DataFrame({'name': b[2], 'lat': b[0], 'lon': b[1]})

"""
Este enfoque no funciona con archivos grandes, el problema esta en commons.read_json_with_encoding cuando se usa
el método ast.literal_eval. No funciona porque la cantidad de memoria usada es demasiado alta.


USO: read_nodes_from_geojson("bogota/urb_sirena_interest_points.geojson")
"""
def read_nodes_from_geojson(filename):
    a = read_json_with_encoding(filename)
    r = []
    for b in a["features"]:
        if "type" in b:
            if "Feature" in b["type"]:
                r.append(b)
    p = []
    for b in r:
        if "properties" in b:
            if "amenity" in b["properties"]:
                p.append(b)
    c = []
    for b in p:
        name = None
        lat = None
        lon = None
        if "name" in b["properties"]:
            name = b["properties"]["name"]
        if b["geometry"]["type"] == "Point":
            lat = b["geometry"]["coordinates"][1]
            lon = b["geometry"]["coordinates"][0]
            geo = None
        else:
            geo = b["geometry"]
        c.append([name, b["properties"]["amenity"], lat, lon, geo])
    x = list(zip(*c))
    z = pd.DataFrame({'name': x[0], 'amenity': x[1], 'lat': x[2], "lon": x[3], "geometry": x[4]})
    return z


"""
pip install ijson

Este paquete no carga todo en memoria.
"""
def read_nodes_overpass_api(filename):
    x = codecs.open(filename, encoding="UTF-8")
    it = ijson.items(x, "elements.item")
    r = []
    for i in it:
        if not "type" in i:
            warnings.warn("there are elements without a type")
            continue
        if not "tags" in i:
            continue
        if not "amenity" in i["tags"]:
            continue
        name = None
        if "name" in i["tags"]:
            name = i["tags"]["name"]
        i["tags"]["amenity"]
        r.append([i["lat"], i["lon"], name, i["tags"]["amenity"]])
    z = list(zip(*r))
    return pd.DataFrame({'lat': z[0], 'lon': z[1], 'name': z[2], "amenity": z[3]})

def load_bogota_interest_points():
    return read_nodes_overpass_api(BOGOTA_INTEREST_POINTS)
