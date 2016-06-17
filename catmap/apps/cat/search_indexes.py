import arrow

from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from haystack import indexes
from haystack.utils.geo import Point

from pinax.eventlog.models import Log

from catmap import TRUTHY
from catmap.apps.shelter.models import Location


class LogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    status = indexes.CharField()
    animal_id = indexes.IntegerField()
    adopter_id = indexes.CharField()
    age_category_at_adoption = indexes.CharField()
    jurisdiction = indexes.CharField()
    suburb_state_post = indexes.CharField()
    outgoing_adoption_date = indexes.DateField()
    received_surrender_date = indexes.DateField()
    surrender_source = indexes.CharField()
    sex = indexes.CharField()
    animal_name = indexes.CharField()
    has_microchip = indexes.BooleanField()
    microchip = indexes.CharField()

    location = indexes.LocationField()

    timestamp = indexes.DateTimeField(model_attr='timestamp')
    action = indexes.CharField(model_attr='action')

    def prepare_status(self, obj):
        return obj.extra.get('status', None)

    def prepare_animal_id(self, obj):
        return obj.extra.get('animal_id', None)

    def prepare_adopter_id(self, obj):
        return obj.extra.get('adopter_id', None)

    def prepare_age_category_at_adoption(self, obj):
        return obj.extra.get('age_category_at_adoption', None)

    def prepare_location(self, obj):
        suburb_state_post = obj.extra.get('suburb_state_post', None)
        if suburb_state_post:
            slug = slugify(suburb_state_post)
            loc = Location.objects.get(slug=slug)
            if loc:
                # return Point(float(loc.lon), float(loc.lat)).geojson
                return "%s,%s" % (loc.lat, loc.lon)
                # return {'lat': loc.lat, 'lon': loc.lon}
        return None

    def prepare_jurisdiction(self, obj):
        return obj.extra.get('jurisdiction', None)

    def prepare_suburb_state_post(self, obj):
        return obj.extra.get('suburb_state_post', None)

    def prepare_outgoing_adoption_date(self, obj):
        date = obj.extra.get('outgoing_adoption_date', None)
        if date:
            return arrow.get(date).datetime
        return None

    def prepare_received_surrender_date(self, obj):
        date = obj.extra.get('received_surrender_date', None)
        if date:
            return arrow.get(date).datetime
        return None

    def prepare_surrender_source(self, obj):
        return obj.extra.get('surrender_source', None)

    def prepare_sex(self, obj):
        return obj.extra.get('sex', None)

    def prepare_animal_name(self, obj):
        return obj.extra.get('animal_name', None)

    def prepare_microchip(self, obj):
        return obj.extra.get('microchip', None)

    def prepare_has_microchip(self, obj):
        return obj.extra.get('microchip', None) is not None

    def get_model(self):
        return Log

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(content_type=ContentType.objects.get(app_label='cat', model='cat'))
