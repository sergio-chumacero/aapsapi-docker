from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from supply_areas.models import SupplyArea

@admin.register(SupplyArea)
class SupplyAreaModelAdmin(LeafletGeoAdmin):
    view_on_site = False
    list_filter= ('epsa',)
    search_fields= ['id','epsa',]
    list_display= ('id','epsa',)

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS: Áreas de Prestación de Serivicios de las EPSA Reguladas'}
        return super(SupplyAreaModelAdmin, self).changelist_view(request, extra_context=extra_context)
