from __future__ import division
import math
import json


## Aggregation processing methods for historical and active databases

# Normalize price of housing to dollars/bedroom
def normalize_price(price, bedrooms):
    return (price / math.floor(bedrooms if bedrooms != 0 else 1))

# Calculates the exponential moving average of pricing data over time
# NOTE: assumes prices are normalized
def calculate_EMAs(raw_data, day_range, out_data):
    temp_ema = 0
    last_ema = raw_data[0]['price']

    def new_EMA(curr_price, day_range, prev_ema):
        k = 2 / (day_range + 1)
        return ((curr_price * k) + (prev_ema * (1 - k)))

    out_data.append({
        'price': last_ema,
        'date_listed': raw_data[0]['date_listed']
    })
    for i in range(1, len(raw_data)):
        temp_ema = new_EMA(raw_data[i]['price'], day_range, last_ema)
        out_data.append({
            'date_listed': raw_data[i]['date_listed'],
            'price': temp_ema
        })
        last_ema = temp_ema

# Calculates average price per neighbourhood on each posting ingestion
# @param (JSON) binned_postings : JSON object holding raycasted postings with the form:
#
#           [{ 'name' : 'NeiName',
#              'positions':
#                  [{bedrooms : int,
#                    price : int,
#                    date_listed : int
#                    latitude : float,
#                    longitude : float,
#                    bathrooms : float,
#                    description : text,
#                    listing_url : text,
#                    listing_id : text,
#                    neighbourhood : text,
#                   },
#                  ]
#             },
#           ]
#
# NOTE: assumes prices are normalized
def avg_neighbourhood_price(binned_postings):
    binned_averages = []
    for hood in binned_postings:
        num_postings = len(hood['positions'])
        binned_averages.append({
            'name': hood['name'],
            'average_price': math.floor(sum([post['price'] for post in hood['positions']]) / num_postings)
        })
    return binned_averages
