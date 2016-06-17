# -*- coding: utf-8 -*-
from rest_framework import serializers

from pinax.eventlog.models import Log

from ..models import Cat


class EventSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    animal_id = serializers.SerializerMethodField()
    adopter_id = serializers.SerializerMethodField()
    age_category_at_adoption = serializers.SerializerMethodField()
    jurisdiction = serializers.SerializerMethodField()
    suburb_state_post = serializers.SerializerMethodField()
    outgoing_adoption_date = serializers.SerializerMethodField()
    sex = serializers.SerializerMethodField()
    animal_name = serializers.SerializerMethodField()
    microchip = serializers.SerializerMethodField()
    date_of = serializers.DateTimeField(source='timestamp')

    class Meta:
        model = Log
        fields = ('status',
                  'animal_id',
                  'adopter_id',
                  'age_category_at_adoption',
                  'jurisdiction',
                  'suburb_state_post',
                  'outgoing_adoption_date',
                  'sex',
                  'animal_name',
                  'microchip',
                  'date_of',)

    def get_status(self, obj):
        return obj.extra.get('status', None)

    def get_animal_id(self, obj):
        return obj.extra.get('animal_id', None)

    def get_adopter_id(self, obj):
        return obj.extra.get('adopter_id', None)

    def get_age_category_at_adoption(self, obj):
        return obj.extra.get('age_category_at_adoption', None)

    def get_jurisdiction(self, obj):
        return obj.extra.get('jurisdiction', None)

    def get_suburb_state_post(self, obj):
        return obj.extra.get('suburb_state_post', None)

    def get_outgoing_adoption_date(self, obj):
        return obj.extra.get('outgoing_adoption_date', None)

    def get_sex(self, obj):
        return obj.extra.get('sex', None)

    def get_animal_name(self, obj):
        return obj.extra.get('animal_name', None)

    def get_microchip(self, obj):
        return obj.extra.get('microchip', None)


class CatSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    age_class = serializers.SerializerMethodField()
    events = EventSerializer(many=True)

    class Meta:
        model = Cat
        fields = ('pk',
                  'name',
                  'age_class',
                  'dob',
                  'age',
                  'gender',
                  'current_status',
                  'breed',
                  'coat_type',
                  'colour',
                  'altered',
                  'desex_done',
                  'shire',
                  'tattoo',
                  'microchip_id',
                  'receipt_id',
                  'animal_notes',
                  # Custom Log Serializer
                  'events',)

    def get_name(self, obj):
        return obj.name if obj.name not in ['', None] else 'No Name'

    def get_age_class(self, obj):
        return 'Kitten' if obj.is_kitten is True else 'Cat'
