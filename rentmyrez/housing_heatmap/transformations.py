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
    last_ema = raw_data[0]['y']

    def new_EMA(curr_price, day_range, prev_ema):
        k = 2 / (day_range + 1)
        return ((curr_price * k) + (prev_ema * (1 - k)))

    out_data.append({
        'y': last_ema,
        'x': raw_data[0]['x']
    })
    for i in range(1, len(raw_data)):
        temp_ema = new_EMA(raw_data[i]['y'], day_range, last_ema)
        out_data.append({
            'x': raw_data[i]['x'],
            'y': temp_ema
        })
        last_ema = temp_ema

# Calculates average price per neighbourhood on each posting ingestion
# NOTE: assumes prices are normalized
def avg_neighbourhood_price(binned_postings):
    binned_averages = []
    for hood in binned_postings:
        num_postings = len(hood['positions'])
        binned_averages.append({
            'name': hood['name'],
            'average_price': math.floor(sum([x['y'] for x in hood['positions']]) / num_postings)
        })

## Testing
#
# raw_data = [{'x': 10, 'y': 10},
#             {'x': 18, 'y': 20},
#             {'x': 24, 'y': 22},
#             {'x': 43, 'y': 45},
#             {'x': 76, 'y': 79},
#             {'x': 99, 'y': 87}]
# out_data = []
# calculate_EMAs(raw_data, 5, out_data)
# pprint(out_data)
#
# with open('../../places/transformation_test.json', 'r+') as t:
#     binned_postings = json.load(t)
#
# avg_neighbourhood_price(binned_postings)
