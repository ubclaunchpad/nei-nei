import grequests
import requests
import sys
import json
from collections import namedtuple
from raycaster import Point, Edge, Polygon, RayCaster

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

def create_polygon(neighbourhood):
    boundary = neighbourhood['boundary']
    edges = []
    for i in range(-1, len(boundary) - 1):
        p1 = Point(x=boundary[i]['longitude'],
                   y=boundary[i]['latitude'])
        p2 = Point(x=boundary[i + 1]['longitude'],
                   y=boundary[i + 1]['latitude'])
        edges.append(Edge(p1, p2))
    return Polygon(neighbourhood['name'], edges)

neighbourhoods = requests.get(neighbourhoods_url, headers={'accept': 'application/json'}).json()
polygons = map(create_polygon, neighbourhoods)

ray_caster = RayCaster(polygons)

points = map(lambda l: Point(x=l['lng'], y=l['lat']), listings)
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
    neighbourhood=p.name if p else None
), zip(listings, map(ray_caster.get_polygon_containing_point, points)))

headers = {'Authorization': 'Token {token}'.format(token=rest_api['token']),
           'Content-Type': 'application/json'}

rs = (grequests.post(listings_url, headers=headers, data=json.dumps(payload)) for payload in payloads)
grequests.map(rs, size=10, exception_handler=lambda r, e: sys.stderr.write(str(e) + '\n'))


#     # change setup (and readme) to make sure that we don't use piping, but instead save files to data folder
#     # Also change crontab
