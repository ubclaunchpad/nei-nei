import grequests
import sys
import json
import xml.etree.ElementTree as ET

config = json.load(open('config.json'))
rest_api = config['rest_api']

if len(sys.argv) > 1:
    neighbourhoods = ET.parse(sys.argv[1])
else:
    import requests
    neighbourhoods_data_url = config['neighbourhoods']['data']['url']
    neighbourhoods = ET.ElementTree(ET.fromstring(requests.get(neighbourhoods_data_url).content))
    neighbourhoods.write('data/raw_neighbourhoods_data.kml')

def get_clean_neighbourhood(n):
    return dict(
        name=n[0].text,
        boundary=map(lambda x: dict(zip(['longitude', 'latitude'], map(float, x.split(',')))),
                     n[3][0][0][0].text.split())
    )

cleaned_neighbourhoods = map(get_clean_neighbourhood, neighbourhoods.getroot()[0][0][2:])

headers = {
    'Authorization': 'Token {token}'.format(token=rest_api['token']),
    'Content-Type': 'application/json'
}

neighbourhoods_url = rest_api['base_url'] + rest_api['neighbourhoods']
rs = (grequests.post(neighbourhoods_url,
                     headers=headers,
                     data=json.dumps(neighbourhood)) for neighbourhood in cleaned_neighbourhoods)
grequests.map(rs, size=10, exception_handler=lambda r, e: sys.stderr.write(str(e) + '\n'))
