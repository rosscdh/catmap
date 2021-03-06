# -*- coding: utf-8 -*-
from django.db import connection
from django.db.models import Min, Max
from django.contrib.contenttypes.models import ContentType

from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import GenericAPIView

from rest_framework_extensions.mixins import ReadOnlyCacheResponseAndETAGMixin

from pinax.eventlog.models import Log

from catmap.apps.cat.models import Cat
from catmap.apps.cat.api.serializers import CatSerializer

from .serializers import DashboardDateRangeSerializer

import datetime
from collections import OrderedDict
from dateutil.rrule import rrule, MONTHLY


cursor = connection.cursor()
# get distinct action names
ACTION_NAMES = OrderedDict((a.lower(), 0) for a in [action[0] for action in cursor.execute("select distinct action from eventlog_log").fetchall()])


class DashboardInitialApiView(ReadOnlyCacheResponseAndETAGMixin, GenericAPIView):
    model = Log

    def get_queryset(self):
        return self.model.objects.all().aggregate(Max('timestamp'), Min('timestamp'))

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        data = {
            'min_date': qs.get('timestamp__min'),
            'max_date': qs.get('timestamp__max'),
        }
        return Response(data)


def _yield_cat_ids(**filters):
    for log in Log.objects.filter(content_type=ContentType.objects.get(app_label='cat', model='cat')).filter(**filters).values('object_id'):
        yield log.get('object_id')


class DashboardApiView(ReadOnlyCacheResponseAndETAGMixin, GenericAPIView):

    def distinct_log_actions(self, **filters):
        # get a full set of month names and year in the range
        months = [dt.strftime('%B, %Y') for dt in rrule(MONTHLY, dtstart=filters.get('timestamp__gte'), until=filters.get('timestamp__lte'))]

        # add the disctinct set of actions to each month
        actions = OrderedDict((m, ACTION_NAMES.copy()) for m in months)
        print filters
        for l in Log.objects.filter(**filters).values('action', 'timestamp'):
            action_type = l.get('action').lower()
            print action_type
            month = l.get('timestamp').strftime('%B, %Y')  # convert to month, year for lookup
            try:
                actions[month][action_type] += 1 # increment the counter
            except KeyError:
                break

        return actions

    def get(self, request, *args, **kwargs):
        date_serializer = DashboardDateRangeSerializer(data=request.GET)

        if date_serializer.is_valid() is False:
            data = date_serializer.errors
            status_code = http_status.HTTP_400_BAD_REQUEST

        else:
            filters = {
                'timestamp__gte': date_serializer.validated_data.get('date_from'),
                'timestamp__lte': date_serializer.validated_data.get('date_to'),
            }
            #import pdb;pdb.set_trace()
            data = {
                'gender': Cat.objects.gender_breakdown(cat_ids=_yield_cat_ids(**filters)),
                'cats': CatSerializer(Cat.objects.filter(pk__in=_yield_cat_ids(**filters)), many=True).data,
                'actions': self.distinct_log_actions(**filters),
            }
            status_code = http_status.HTTP_200_OK
        return Response(data, status=status_code)
