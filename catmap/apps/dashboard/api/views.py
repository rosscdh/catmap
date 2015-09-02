# -*- coding: utf-8 -*-
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
            }
            status_code = http_status.HTTP_200_OK
        return Response(data, status=status_code)
