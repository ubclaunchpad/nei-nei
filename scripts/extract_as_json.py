import sqlite3
import json
import sys
import os

sys.path.append(os.path.abspath('../rentmyrez/housing_heatmap'))
print(sys.path)
from casting import RayCaster, organize_polygons
from transformations import *

def transform_to_dict(db_data):
    return map(lambda datum: dict(
            latitude=datum[0],
            longitude=datum[1],
            date_listed=int(datum[3]),
            price=normalize_price(datum[2], datum[4]),
            bedrooms=datum[4]
            ), db_data)

def query(db_path):
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT latitude, longitude, price, date_listed, bedrooms FROM pm_api_listings')
        posting_db_info = cursor.fetchall()
    except sqlite3.Error as e:
        print("Error selecting posting_db_info: "+str(e.args[0]))
    finally:
        connection.close()
        assert(len(posting_db_info) > 0)
        return transform_to_dict(posting_db_info)

# Grab data from DB, cast within neighbourhoods, and transform for dashboard
polygons = []
with open('../places/polygons.json', 'r+') as p:
    polygon_data = json.load(p)
    print("Organizing lat,lon points into polygons...")
    organize_polygons(polygon_data, polygons)

print("Querying DB for postings...")
database_path = '/home/estro/Projects/pm-api-cron/pm_api_listings.db'
in_list = query(database_path)
out_list = []

print("Placing postings into polygons...")
RayCaster.place_pos_in_polygon(in_list, polygons, out_list)
with open('../places/dashboard_test_data.json', 'w+') as t:
    json.dump(out_list, t)
# with open('ema_data.json', 'w+') as e:
#     temp = []
#     calculate_EMAs(out_list, 25, temp)
#     json.dump(temp, e)
#     del temp[]
del out_list
del polygons
print("Done!")
