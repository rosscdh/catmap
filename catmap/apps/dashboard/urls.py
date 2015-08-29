from django.conf.urls import include, url

from .views import DashboardView

urlpatterns = [
    url(r'^admin/dashboard/$', DashboardView.as_view(), name='admin-default'),
]