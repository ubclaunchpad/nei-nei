import requests
import sys
import json
import xml.etree.ElementTree as ET

config = json.load(open('config.json'))
rest_api = config['rest_api']

if len(sys.argv) > 1:
    neighbourhoods = ET.parse(sys.argv[1])
else:
    import requests
    from datetime import datetime
    neighbourhoods_data_url = config['neighbourhoods']['data']['url']
    neighbourhoods = ET.ElementTree(ET.fromstring(requests.get(neighbourhoods_data_url).content))
    neighbourhoods.write('data/neighbourhoods_{date}.kml'.format(date=datetime.today().strftime('%Y-%m-%d_%H-%M')))

def get_clean_neighbourhood(n):
    return dict(
        name=n[0].text,
        boundary=map(lambda x: dict(zip(['longitude', 'latitude'], map(float, x.split(',')))),
                     n[3][0][0][0].text.split())
    )

cleaned_neighbourhoods = map(get_clean_neighbourhood, neighbourhoods.getroot()[0][0][2:])

headers = {
    'Authorization': 'Token {token}'.format(token=rest_api['credentials']['token']),
    'Content-Type': 'application/json'
}

neighbourhoods_url = rest_api['base_url'] + rest_api['neighbourhoods']
for n in cleaned_neighbourhoods:
    r = requests.post(neighbourhoods_url, headers=headers, data=json.dumps(n))
    print(r.text)
