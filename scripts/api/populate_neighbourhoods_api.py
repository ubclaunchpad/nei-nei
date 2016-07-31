import grequests
import sys
import json

def get_clean_neighbourhood(n):
    return {
        'name': n['name'],
        'boundary': map(lambda x: dict(zip(['longitude', 'latitude'], map(float, x.split(',')))),
                        n['Polygon']['outerBoundaryIs']['LinearRing']['coordinates'].split())
    }

neighbourhoods = json.load(open(sys.argv[1], 'r'))
cleaned_neighbourhoods = map(get_clean_neighbourhood, neighbourhoods)

def exception_handler(request, exception):
    print str(exception)

rest_api = json.load(open('config.json'))['rest_api']
headers = {'Accept': 'application/json',
           'Authorization': 'Token {token}'.format(token=rest_api['token']),
           'Content-Type': 'application/json'}


neighbourhoods_url = rest_api['base_url'] + rest_api['neighbourhoods']
rs = (grequests.post(neighbourhoods_url,
                     headers=headers,
                     data=json.dumps(neighbourhood)) for neighbourhood in cleaned_neighbourhoods)
grequests.map(rs, size=10, exception_handler=exception_handler)
