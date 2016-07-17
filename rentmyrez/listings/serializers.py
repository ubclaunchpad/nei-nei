from rest_framework import serializers
from listings.models import Listing

# TODO: save date_listed as actual date

class ListingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Listing
        fields = ('url', 'latitude', 'longitude', 'price', 'date_listed',
                  'bedrooms', 'bathrooms', 'description', 'listing_url', 'listing_id', 'address')
