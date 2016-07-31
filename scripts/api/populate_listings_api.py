import grequests
import requests
import sys
import json
from collections import namedtuple
from raycaster import Point, Edge, Polygon, RayCaster

listings = json.load(open(sys.argv[1], 'r'))
rest_api = json.load(open('config.json'))['rest_api']
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

def exception_handler(request, exception):
    print str(exception)

headers = {'Authorization': 'Token {token}'.format(token=rest_api['token']),
           'Content-Type': 'application/json'}

rs = (grequests.post(listings_url, headers=headers, data=json.dumps(payload)) for payload in payloads)
grequests.map(rs, size=10, exception_handler=exception_handler)


#     # change setup (and readme) to make sure that we don't use piping, but instead save files to data folder
#     # Also change crontab
#     pass
