from housing_heatmap.models import House
from rest_framework import serializers

class HouseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = House
        fields = ('latitude', 'longitude', 'num_bedrooms', 'square_footage',
                  'rent', 'posting_url', 'address', 'posted', 'id')
