from rest_framework import serializers
from neighbourhoods.models import Neighbourhood
from rest_framework.serializers import ValidationError

class CoordinateField(serializers.DictField):
    def to_internal_value(self, data):
        data = super(CoordinateField, self).to_internal_value(data)
        if not ('latitude' in data and 'longitude' in data):
            raise ValidationError('Coordinate is improperly formatted.')
        return data

class NeighbourhoodSerializer(serializers.HyperlinkedModelSerializer):
    boundary = serializers.ListField(
        child=CoordinateField(child=serializers.FloatField())
    )
    class Meta:
        model = Neighbourhood
        fields = ('url', 'name', 'boundary')
