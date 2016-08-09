from rest_framework import serializers
from listings.models import Listing, Neighbourhood
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
    listings = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='listing-detail',
        read_only=True
    )
    class Meta:
        model = Neighbourhood
        fields = ('url', 'name', 'boundary', 'listings')

# TODO: save date_listed as actual date
class ListingSerializer(serializers.HyperlinkedModelSerializer):
    neighbourhood = serializers.SlugRelatedField(
        required=False,
        allow_null=True,
        slug_field='name',
        queryset=Neighbourhood.objects.all()
    )
    class Meta:
        model = Listing
        fields = ('url', 'latitude', 'longitude', 'neighbourhood', 'price', 'date_listed',
                  'bedrooms', 'bathrooms', 'description', 'listing_url', 'listing_id', 'address')
