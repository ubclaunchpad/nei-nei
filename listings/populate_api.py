import sys
import json

from twisted.internet import reactor
from twisted.internet import defer
from twisted.web.client import Agent
from twisted.web.http_headers import Headers


def main():
    infile = open(sys.argv[1], 'r') if len(sys.argv) > 1 else sys.stdin
    listings = json.load(infile)
    rest_endpoint = json.load(open('config.json'))['rest_endpoint']

    def got_response(resp):
        print resp # for debugging

    ds = []

    for listing in listings:
        agent = Agent(reactor)
        d = agent.request(
            'POST',
            rest_endpoint,
            Headers({'Accept': ['application/json']}),
            None) # TODO
        d.addCallbacks(got_response)
        ds.append(d)

    dlist = defer.DeferredList(ds, consumeErrors=True)
    dlist.addCallback(lambda res : reactor.stop())

    reactor.run()


if __name__ == '__main__':
    main()
