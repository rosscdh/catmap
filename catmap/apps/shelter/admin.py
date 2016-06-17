from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Shelter, Location


class LocationAdmin(ImportExportModelAdmin):
    resource_class = Location

    list_display = ('name',
                    'jurisdiction',
                    'lat',
                    'lon',
                    'altitude')

    search_fields = ['id', 'name', 'jurisdiction']


admin.site.register(Location, LocationAdmin)
admin.site.register([Shelter])
