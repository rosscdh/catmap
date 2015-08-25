from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Cat
from pinax.eventlog.models import Log


class LogInline(GenericTabularInline):
    model = Log
    extra = 1
    can_delete = False


class CatAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',
                    'microchip_id',
                    'receipt_id',
                    'adopted_from',
                    'returned',
                    'current_status',)
    list_filter = ('sex', 'prev_desex', 'altered', 'desex_done', 'returned', 'current_status')
    search_fields = ['id', 'name', 'microchip_id', 'receipt_id', 'adopted_from', 'current_status']
    inlines = [LogInline,]


admin.site.register(Cat, CatAdmin)
