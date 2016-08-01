import grequests
import requests
import sys
import json

config = json.load(open('config.json'))
rest_api = config['rest_api']

if len(sys.argv) > 1:
    listings = json.load(open(sys.argv[1]))
else:
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
    json.dump(listings, open('data/raw_listings_data.json', 'w'))

listings_url = rest_api['base_url'] + rest_api['listings']
neighbourhoods_url = rest_api['base_url'] + rest_api['neighbourhoods']
neighbourhoods = requests.get(neighbourhoods_url).json()

from geometry import Point, Polygon

polygons = map(lambda n: Polygon([(c['longitude'], c['latitude']) for c in n['boundary']], name=n['name']), neighbourhoods)
points = (Point(x=l['lng'], y=l['lat']) for l in listings)
find_polygon_containing_point = lambda point: next((p for p in polygons if p.intersects(point)), None)

payloads = map(lambda (l, p): dict(
    latitude=l['lat'],
    longitude=l['lng'],
    bedrooms=int(l['beds']),
    bathrooms=int(l['baths']),
    description=l['description'],
    listing_url=l['url'],
    listing_id=l['id'],
    address=l['location'],
    price=int(l['price']),
    date_listed=l['date'],
    neighbourhood=p and p.name
), zip(listings, map(find_polygon_containing_point, points)))

headers = {
    'Authorization': 'Token {token}'.format(token=rest_api['credentials']['token']),
    'Content-Type': 'application/json'
}

rs = (grequests.post(listings_url, headers=headers, data=json.dumps(payload)) for payload in payloads)
grequests.map(rs, size=10, exception_handler=lambda r, e: sys.stderr.write(str(e) + '\n'))
