from django.core.management.base import BaseCommand
from listings.models import Listing
from django.utils import timezone

class Command(BaseCommand):

    help = 'Expires listing objects which are out-of-date'

    def handle(self, *args, **options):
        self.stdout.write(
            str(Listing.objects.filter(created__lt=timezone.now() - timezone.timedelta(days=14)).delete())
        )
