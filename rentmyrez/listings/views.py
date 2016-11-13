from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from listings.models import Listing, Neighbourhood, HistoricalListings
from listings.serializers import ListingSerializer, NeighbourhoodSerializer, HistoricalListingsSerializer

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

class NeighbourhoodViewSet(viewsets.ModelViewSet):
    queryset = Neighbourhood.objects.all()
    serializer_class = NeighbourhoodSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

class HistoricalListingsViewSet(viewsets.ModelViewSet):
    queryset = HistoricalListings.objects.all()
    serializer_class = HistoricalListingsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)