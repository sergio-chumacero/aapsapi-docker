from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from ambiental.models import SARH, TecnicalDataSub, TecnicalDataSup

class TecnicalDataSubInline(admin.StackedInline):
    model = TecnicalDataSub
    extra = 1

class TecnicalDataSupInline(admin.StackedInline):
    model = TecnicalDataSup
    extra = 1

@admin.register(SARH)
class SARHModelAdmin(LeafletGeoAdmin):
    view_on_site = False
    list_filter= ('epsa', 'state', 'epsa','municipality','sub_subt')
    search_fields= ['epsa','user']
    list_display = ('sarh_id','epsa','user','get_state','municipality','get_sub_subt')

    inlines = [TecnicalDataSubInline,TecnicalDataSupInline]

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS: Sistemas de Autoabastecimiento de Recursos Hídricos (SARH).'}
        return super(SARHModelAdmin, self).changelist_view(request, extra_context=extra_context)



