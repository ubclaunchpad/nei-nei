from django.shortcuts import render

from housing_heatmap.models import House
from rest_framework import viewsets
from housing_heatmap.serializers import HouseSerializer

class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all().order_by('-posted')
    serializer_class = HouseSerializer
