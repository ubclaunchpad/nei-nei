import grequests
import requests
import sys
import json

config = json.load(open('config.json'))
rest_api = config['rest_api']

if len(sys.argv) > 1:
    listings = json.load(open(sys.argv[1]))
else:
    def getListingsData(url, ids):
        limit = 300
        batches = [ids[i:i+limit] for i in range(0, len(ids), limit)]
        reqs = (grequests.post(url, headers={'accept': 'application/json'}, data={'ids': ','.join(batch)}, params={'getBuilding': True}) for batch in batches)
        return reduce(lambda x, y: x + y.json(), grequests.imap(reqs), [])

    def getListingIds(url, payload):
        req = requests.get(url, params={k: json.dumps(v) for k, v in payload.items()}, headers={'accept': 'application/json'})
        return map(lambda x: x['id'], req.json())

    ids = getListingIds(config['listing_ids_url'], config['listings_search_criteria'])
    listings = getListingsData(config['listings_url'], ids)
    json.dump(listings, open('data/raw_listings_data.json', 'w'))

listings_url = rest_api['base_url'] + rest_api['listings']
neighbourhoods_url = rest_api['base_url'] + rest_api['neighbourhoods']
neighbourhoods = requests.get(neighbourhoods_url, headers={'accept': 'application/json'}).json()

from geometry import Point, Polygon

polygons = (Polygon(map(lambda c: (c['longitude'], c['latitude']), n['boundary']), name=n['name']) for n in neighbourhoods)
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

headers = {'Authorization': 'Token {token}'.format(token=rest_api['token']),
           'Content-Type': 'application/json'}

rs = (grequests.post(listings_url, headers=headers, data=json.dumps(payload)) for payload in payloads)
grequests.map(rs, size=10, exception_handler=lambda r, e: sys.stderr.write(str(e) + '\n'))
