import sys
import json

from StringIO import StringIO

from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet import protocol
from twisted.web.client import Agent
from twisted.web.client import FileBodyProducer
from twisted.web.http_headers import Headers


def main():
    infile = open(sys.argv[1], 'r') if len(sys.argv) > 1 else sys.stdin
    listings = json.load(infile)
    rest_api = json.load(open('config.json'))['rest_api']
    success = []

    def handle_response(response, id):
        print 'Response code: {0}'.format(response.code)
        if response.code == 201:
            success.append(id)

    def handle_failure(failure):
        print failure.getErrorMessage()

    ds = []

    print 'Inserting {0} listings'.format(len(listings))
    for listing in listings:
        agent = Agent(reactor)
        payload = dict(
            latitude=listing['lat'],
            longitude=listing['lng'],
            bedrooms=int(listing['beds']),
            bathrooms=int(listing['baths']),
            description=listing['description'],
            listing_url=listing['url'],
            listing_id=listing['id'],
            address=listing['location'],
            price=int(listing['price']),
            date_listed=listing['date']
        )

        d = agent.request(
            'POST',
            str(rest_api['url']),
            Headers({'Accept': ['application/json'],
                     'Authorization': ['Token {token}'.format(token=rest_api['token'])],
                     'Content-Type': ['application/json']}),
            FileBodyProducer(StringIO(json.dumps(payload))))
        d.addCallbacks(handle_response, handle_failure, callbackArgs={'id': listing['id']})
        ds.append(d)

    dlist = defer.DeferredList(ds)
    dlist.addCallback(lambda res : reactor.stop())

    reactor.run()
    print 'Successfully completed: {0}/{1}'.format(len(success), len(listings))


if __name__ == '__main__':
    main()
