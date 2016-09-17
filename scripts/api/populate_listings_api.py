import grequests
import requests
import sys
import json

config = json.load(open('config.json'))
rest_api = config['rest_api']

if len(sys.argv) > 1:
    listings = json.load(open(sys.argv[1]))
else:
    from datetime import datetime

    def getListingsData(url, params, ids):
        limit = 300
        batches = (ids[i:i+limit] for i in range(0, len(ids), limit))
        headers = {
            'accept': 'application/json'
        }
        reqs = (grequests.post(url, headers=headers, params=params, data={'ids': ','.join(batch)}) for batch in batches)
        return reduce(lambda x, y: x + y.json(), grequests.imap(reqs), [])

    def getListingsIds(url, params):
        headers = {
            'accept': 'application/json'
        }
        req = requests.get(url, headers=headers, params={k: json.dumps(v) for k, v in params.items()})
        return map(lambda x: x['id'], req.json())

    listings_ids = config['listings']['ids']
    listings_data = config['listings']['data']
    ids = getListingsIds(listings_ids['url'], listings_ids['params'])
    listings = getListingsData(listings_data['url'], listings_data['params'], ids)
    json.dump(listings, open('data/listings_{date}.json'.format(date=datetime.today().strftime('%Y-%m-%d_%H-%M')), 'w'))

listings_url = rest_api['base_url'] + rest_api['listings']
neighbourhoods_url = rest_api['base_url'] +  rest_api['neighbourhoods']
neighbourhoods = requests.get(neighbourhoods_url).json()

# Cast the listings into neighbourhoods
from casting import RayCaster, organize_polygons

print("Starting casting...")
polygons = []
cast_listings = []
organize_polygons(neighbourhoods, polygons)
RayCaster.place_pos_in_polygon(listings, polygons, cast_listings)
del polygons

print("Casting complete. Begin writing payload...")

payloads = []
for hood in cast_listings:
    payloads.extend(map(lambda p: dict(
        latitude=float(p['lat']),
        longitude=float(p['lng']),
        bedrooms=int(p['beds']),
        bathrooms=int(p['baths']),
        description=p['description'],
        listing_url=p['url'],
        listing_id=p['id'],
        address=p['location'],
        price=int(p['price']),
        date_listed=p['date'],
        neighbourhood=hood['name']
    ), hood['positions']))
del cast_listings

print("Payload formatting complete. Sending...")

headers = {
    'Authorization': 'Token {token}'.format(token=rest_api['credentials']['token']),
    'Content-Type': 'application/json'
}

rs = (grequests.post(listings_url, headers=headers, data=json.dumps(payload)) for payload in payloads)
grequests.map(rs, size=10, exception_handler=lambda r, e: sys.stderr.write(str(e) + '\n'))

print("Payload sent!")
