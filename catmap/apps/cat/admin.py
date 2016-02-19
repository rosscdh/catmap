from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from import_export import resources
from import_export import fields as import_export_fields
from import_export.admin import ImportExportModelAdmin

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
        return '%s %s (%s)' % (cat.owner.first_name, cat.owner.last_name, cat.owner.email)



class LogInline(GenericTabularInline):
    model = Log
    extra = 1
    can_delete = False


class CatAdmin(ImportExportModelAdmin):
    resource_class = CatResource
    list_display = ('__unicode__',
                    'microchip_id',
                    'receipt_id',
                    'adopted_from',
                    'shire',
                    'returned',
                    'current_status',
                    'events')
    list_filter = ('sex', 'prev_desex', 'altered', 'desex_done', 'returned', 'current_status')
    search_fields = ['id', 'name', 'microchip_id', 'receipt_id', 'adopted_from', 'shire', 'current_status']
    inlines = [LogInline,]

    def events(self, obj):
        return JSONRenderer().render(EventSerializer(obj.events, many=True).data)

admin.site.register(Cat, CatAdmin)
