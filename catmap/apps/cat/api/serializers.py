# -*- coding: utf-8 -*-
from rest_framework import serializers

from pinax.eventlog.models import Log

from ..models import Cat


class EventSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    lost_found_address = serializers.SerializerMethodField()
    date_of = serializers.DateTimeField(source='timestamp')

    class Meta:
        model = Log
        fields = ('status',
                  'source',
                  'lost_found_address',
                  'date_of')

    def get_status(self, obj):
        if obj.extra.get('sub_status', None) not in ['', None]:
            return '%s %s' % (obj.extra.get('status'), obj.extra.get('sub_status'))
        return obj.extra.get('status')

    def get_source(self, obj):
        return obj.extra.get('source', None)

    def get_lost_found_address(self, obj):
        return obj.extra.get('lost_found_address', None)


class CatSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    events = EventSerializer(many=True)

    class Meta:
        model = Cat
        fields = ('pk',
                  'name',
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
