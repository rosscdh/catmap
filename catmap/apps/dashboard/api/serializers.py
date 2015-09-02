# -*- coding: utf-8 -*-
from rest_framework import serializers

from datetime import datetime


class DashboardDateRangeSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    def validate_date_from(self, value):
        return datetime.combine(value, datetime.min.time())

    def validate_date_to(self, value):
        return datetime.combine(value, datetime.min.time())
