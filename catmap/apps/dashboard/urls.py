# -*- coding: utf-8 -*-
from rest_framework import routers
from django.conf.urls import include, url

from .api.views import DashboardInitialApiView, DashboardApiView
from .views import DashboardView

urlpatterns = [
  # api
  url(r'^api/v1/dashboard/initial$', DashboardInitialApiView.as_view(), name='api:dashboard-initial'),
  url(r'^api/v1/dashboard$', DashboardApiView.as_view(), name='api:dashboard'),
  # dash angular view
  url(r'^admin/dashboard/$', DashboardView.as_view(), name='admin-default'),
]
