from django.core.management.base import BaseCommand
from listings.models import Listing
from django.utils import timezone
from collections import defaultdict
import numpy as np

class Command(BaseCommand):

    help = 'Aggregates weekly data'

    def handle(self, *args, **options):
        listings = Listing.objects.filter(created__gt=timezone.now() - timezone.timedelta(days=7))
        nbhds = defaultdict(list)
        for l in listings:
            nbhds[l.neighbourhood] += [l]
        results = map(self._mapper, nbhds.items())
        map(self.stdout.write, map(str, results))

    @staticmethod
    def _mapper((neighbourhood, listings)):
        prices = map(lambda l: l.price, listings)
        bedrooms = map(lambda l: l.bedrooms, listings)
        return dict(
            neighbourhood=neighbourhood and neighbourhood.name,
            average_price=np.mean(prices),
            median_price=np.median(prices),
            price_range=np.max(prices) - np.min(prices),
            average_bedrooms=np.mean(bedrooms),
            first_q_percent=np.percentile(prices, 25),
            third_q_percent=np.percentile(prices, 75),
        )
