from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

import datetime

from import_export import resources
from import_export import fields as import_export_fields
from import_export.admin import ImportExportModelAdmin

from daterange_filter.filter import DateRangeFilter, clean_input_prefix, FILTER_PREFIX

from rest_framework.renderers import JSONRenderer

from .models import Cat
from .api.serializers import EventSerializer

from pinax.eventlog.models import Log


class CatResource(resources.ModelResource):
    events = import_export_fields.Field()
    gender = import_export_fields.Field()
    is_kitten = import_export_fields.Field()
    age = import_export_fields.Field()
    owner = import_export_fields.Field()

    class Meta:
        model = Cat
        fields = ('id',
                  'name',
                  'dob',
                  'age',
                  'gender',
                  'breed',
                  'coat_type',
                  'colour',
                  'current_status',
                  'date_adopted',
                  'is_kitten',
                  'altered',
                  'prev_desex',
                  'desex_done',
                  'shire',
                  'tattoo',
                  'microchip_id',
                  'receipt_id',
                  'adopted_from',
                  'returned',
                  'adoption_notes',
                  'animal_notes',
                  'owner',
                  'events',)
        export_order = fields

    def dehydrate_events(self, cat):
        return JSONRenderer().render(EventSerializer(cat.events, many=True).data)

    def dehydrate_gender(self, cat):
        return cat.sex

    def dehydrate_is_kitten(self, cat):
        return cat.is_kitten

    def dehydrate_age(self, cat):
        return cat.age

    def dehydrate_owner(self, cat):
        if cat.owner:
            return '%s %s (%s)' % (cat.owner.first_name, cat.owner.last_name, cat.owner.email)
        else:
            return 'No Owner'


class EventListFilter(admin.SimpleListFilter):
    title = 'Event'
    parameter_name = 'event'

    def lookups(self, request, model_admin):
        choices = Cat.objects.all().values_list('current_status', flat=True).distinct()
        return zip(choices, choices)

    def queryset(self, request, queryset):
        event = self.used_parameters.get(self.parameter_name)
        if event:
            affected_pks = Log.objects.filter(extra__icontains={'status': event}).values_list('object_id', flat=True).distinct()
            if affected_pks:
                return queryset.filter(pk__in=affected_pks) | queryset.filter(current_status=event)
        else:
            return queryset


class EventDateFilter(DateRangeFilter):
    title = 'Event Date'
    parameter_name = 'event_date'
    field_path = 'timestamp'

    def __init__(self, *args, **kwargs):
        super(EventDateFilter, self).__init__(*args, **kwargs)
        self.field_path = 'timestamp'

    def queryset(self, request, queryset):
        if self.form.is_valid():
            # get no null params
            filter_params = clean_input_prefix(dict(filter(lambda x: bool(x[1]), self.form.cleaned_data.items())))

            filter_params['timestamp__lte'] = filter_params.pop('fake_date_event__lte', None)
            filter_params['timestamp__gte'] = filter_params.pop('fake_date_event__gte', None)

            if filter_params['timestamp__lte'] is None:
                filter_params.pop('timestamp__lte', None)
            if filter_params['timestamp__gte'] is None:
                filter_params.pop('timestamp__gte', None)
            if filter_params:
                # filter by upto included
                # lookup_upto = self.lookup_kwarg_upto.lstrip(FILTER_PREFIX)
                # if filter_params.get(lookup_upto) is not None:
                #     lookup_kwarg_upto_value = filter_params.pop(lookup_upto)
                #     filter_params['timestamp__lt'] = lookup_kwarg_upto_value + datetime.timedelta(days=1)
                affected_pks = Log.objects.filter(**filter_params).values_list('object_id', flat=True).distinct()

                return queryset.filter(pk__in=affected_pks)
        else:
            return queryset


class LogInline(GenericTabularInline):
    model = Log
    extra = 1
    can_delete = False


class CatAdmin(ImportExportModelAdmin):
    resource_class = CatResource

    list_display = ('__unicode__',
                    'gender',
                    'microchip_id',
                    'receipt_id',
                    'adopted_from',
                    'date_adopted',
                    'shire',
                    #'returned',
                    'current_status',
                    'events')

    list_filter = (('fake_date_event', EventDateFilter),
                    EventListFilter,
                    ('date_adopted', DateRangeFilter),
                    'sex',
                    'prev_desex',
                    'altered',
                    'desex_done',
                    'returned',)
                    #'current_status',)
    search_fields = ['id', 'name', 'microchip_id', 'receipt_id', 'adopted_from', 'shire', 'current_status']
    inlines = [LogInline,]

    def events(self, obj):
        return JSONRenderer().render(EventSerializer(obj.events, many=True).data)

admin.site.register(Cat, CatAdmin)
