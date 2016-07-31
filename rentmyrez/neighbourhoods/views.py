from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from neighbourhoods.models import Neighbourhood
from neighbourhoods.serializers import NeighbourhoodSerializer

class NeighbourhoodViewSet(viewsets.ModelViewSet):
    queryset = Neighbourhood.objects.all()
    serializer_class = NeighbourhoodSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
