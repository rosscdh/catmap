from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
User = get_user_model()

from pinax.eventlog.models import Log

from catmap import TRUTHY
from catmap.apps.shelter.models import Location

from geopy.geocoders import Nominatim
geolocator = Nominatim()


class Command(BaseCommand):
    help = 'Setup locatons based on Log objects'

    def handle(self, *args, **options):
        for l in Log.objects.all().iterator():
            suburb_state_post = l.extra.get('suburb_state_post', None)
            jurisdiction = l.extra.get('jurisdiction', None)

            if suburb_state_post:
                location, is_new = Location.objects.get_or_create(slug=slugify(suburb_state_post))
                if is_new is True or 1:
                    print suburb_state_post
                    location.name = suburb_state_post.strip() if location.name is None else None
                    location.jurisdiction = jurisdiction.strip() if location.jurisdiction is None else None

                    if location.lat is None or location.lon is None:
                        loc = geolocator.geocode(location.name)
                        if loc:
                            location.lat = loc.latitude
                            location.lon = loc.longitude
                            location.altitude = loc.altitude

                    location.save()


