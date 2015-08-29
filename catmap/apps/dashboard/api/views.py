# -*- coding: utf-8 -*-
from django.db.models import Min, Max

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from pinax.eventlog.models import Log


class DashboardInitialApiView(GenericAPIView):
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


class DashboardApiView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        data = {
        }
        return Response(data)
