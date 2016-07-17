import grequests
import sys
import json

infile = open(sys.argv[1], 'r') if len(sys.argv) > 1 else sys.stdin
listings = json.load(infile)
rest_api = json.load(open('config.json'))['rest_api']

def exception_handler(request, exception):
    print str(exception)

headers = {'Accept': 'application/json',
           'Authorization': 'Token {token}'.format(token=rest_api['token']),
           'Content-Type': 'application/json'}

payloads = map(lambda l: dict(
    latitude=l['lat'],
    longitude=l['lng'],
    bedrooms=int(l['beds']),
    bathrooms=int(l['baths']),
    description=l['description'],
    listing_url=l['url'],
    listing_id=l['id'],
    address=l['location'],
    price=int(l['price']),
    date_listed=l['date']
), listings)

rs = (grequests.post(rest_api['url'], headers=headers, data=json.dumps(payload)) for payload in payloads)
grequests.map(rs, size=10, exception_handler=exception_handler)
