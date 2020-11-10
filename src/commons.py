# -*- coding: utf-8 -*-
# +
## Utilidades comunes entre places y OSM.

# +
import csv
import ast
import codecs

from math import cos, asin, sqrt


# +
def read_csv_with_encoding(filename, delimiter="|", encoding="iso-8859-1"):
    with codecs.open(filename, encoding=encoding) as fp:
        reader = csv.reader(fp, delimiter=delimiter)
        csvFile = list(reader)
        return pd.DataFrame(csvFile[1:], columns=csvFile[0])
    
def read_json_with_encoding(filename, encoding="iso-8859-1"):
    with codecs.open(filename, encoding=encoding) as a:
        l = a.read()
        json_file = ast.literal_eval(l)
        return json_file
# -



import pandas as pd


def distance(lat1, lon1, lat2, lon2):
    """
    El resultado de la medición de distancia esta en kilometros.
    """
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))


def build_center_point(df):
    lat = df["latitude"].mean()
    lon = df["longitude"].mean()
    return pd.DataFrame({'fid': [777], 'latitude': [lat], 'longitude': [lon]})


"""
El proceso es muy pesado y no es posible hacer el ananlisis con toda la data de bogotá, el número de registros es
demasiado grande para caber en memoria. El uso correcto es filtrar los datos antes de hacer el cross join.
"""
def compute_cross_distances(location_df, interest_points_df=None):
    condition_latitude = ~location_df["latitude"].isna()
    condition_longitude = ~location_df["longitude"].isna()
    location_df_complete = location_df.loc[condition_latitude & condition_longitude]
    results = []
    for i in location_df_complete.index:
        for j in interest_points_df.index:
            results.append([
                location_df_complete.loc[i, "fid"],
                distance(location_df_complete.loc[i, "latitude"], 
                                 location_df_complete.loc[i, "longitude"], 
                                float(interest_points_df.loc[j, "lat"]), float(interest_points_df.loc[j, "lon"])),
                location_df_complete.loc[i, "latitude"],
                location_df_complete.loc[i, "longitude"],
                interest_points_df.loc[j, "lat"],
                interest_points_df.loc[j, "lon"],
                interest_points_df.loc[j, "amenity"],
                interest_points_df.loc[j, "name"]
            ])
    final = list(zip(*results))
    return pd.DataFrame({'fid': final[0], 'distance': final[1], 'p_lat': final[2], 
                         'p_lon': final[3], 'i_lat': final[4], 'i_lon': final[5],
                         'amenity': final[6], 'name': final[7]})
