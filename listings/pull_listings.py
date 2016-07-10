import requests
import json
import functools
import sys

def getListingData(url, ids):
    def getListingSubsetData(chunk):
        req = requests.Request('POST', url, params={'getBuilding': True}, data={'ids': ','.join(chunk)}, headers={'accept': 'application/json'})
        prepared = req.prepare()
        s = requests.Session()
        response = s.send(prepared)
        return response.json()

    limit = 300
    return functools.reduce(lambda x, y: x + getListingSubsetData(y), [ids[i:i+limit] for i in range(0, len(ids), limit)], [])

def getListingIds(url, payload):
    req = requests.Request('GET', url, params={k: json.dumps(v) for k, v in payload.items()}, headers={'accept': 'application/json'})
    prepared = req.prepare()
    s = requests.Session()
    response = s.send(prepared)
    return list(map(lambda x: x['id'], response.json()))


if __name__ == '__main__':
    config = json.load(open('config.json'))
    ids = getListingIds(config['ids_url'], config['search_criteria'])
    listings = getListingData(config['listings_url'], ids)
    json.dump(listings, open(sys.argv[1], 'w') if len(sys.argv) > 1 else sys.stdout)
