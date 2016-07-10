import requests
import grequests
import json
import sys

def getListingData(url, ids):
    limit = 300
    chunks = [ids[i:i+limit] for i in range(0, len(ids), limit)]
    reqs = (grequests.post(url, headers={'accept': 'application/json'}, data={'ids': ','.join(chunk)}, params={'getBuilding': True}) for chunk in chunks)
    return reduce(lambda x, y: x + y.json(), grequests.imap(reqs), [])

def getListingIds(url, payload):
    req = requests.get(url, params={k: json.dumps(v) for k, v in payload.items()}, headers={'accept': 'application/json'})
    return map(lambda x: x['id'], req.json())


if __name__ == '__main__':
    config = json.load(open('config.json'))
    ids = getListingIds(config['ids_url'], config['search_criteria'])
    listings = getListingData(config['listings_url'], ids)
    json.dump(listings, open(sys.argv[1], 'w') if len(sys.argv) > 1 else sys.stdout)
