from django.contrib import admin
from performance import models

@admin.register(models.EPSA)
class EPSAModelAdmin(admin.ModelAdmin):
    view_on_site = False
    list_filter = ('category', 'state',)
    search_fields = ['code', 'name', 'state',]
    list_display = ('code', 'name', 'state', 'category',)

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS - Seguimiento Regulatorio: EPSAs'}
        return super(EPSAModelAdmin, self).changelist_view(request, extra_context=extra_context)

@admin.register(models.Variable)
class VariableModelAdmin(admin.ModelAdmin):
    view_on_site = False
    list_filter = ('var_type',)
    search_fields = ['name', 'code','var_type',]
    list_display = ('code', 'var_id', 'name', 'var_type', 'unit',)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS - Seguimiento Regulatorio: Variables'}
        return super(VariableModelAdmin, self).changelist_view(request, extra_context=extra_context)

@admin.register(models.Indicator)
class IndicatorModelAdmin(admin.ModelAdmin):
    view_on_site = False
    list_filter = ('criteria',)
    search_fields = ['name', 'code', 'criteria',]
    list_display = ('code', 'ind_id', 'name', 'criteria', 'unit',)
    
    fields_list = [('code',), ('name',), ('criteria'), ('unit'),]
    for cat in ['A', 'B', 'C', 'D']:
        fields_list.append((f'par_min_{cat}', f'par_max_{cat}'))
    fields = tuple(fields_list)

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS - Seguimiento Regulatorio: Indicadores'}
        return super(IndicatorModelAdmin, self).changelist_view(request, extra_context=extra_context)

@admin.register(models.VariableReport)
class VariableReportModelAdmin(admin.ModelAdmin):
    view_on_site = False
    list_filter = ('year', 'epsa')
    search_fields = ['epsa', 'year', 'month']
    list_display = ('epsa', 'year', 'month', 'get_category', 'get_state',)
    fields_list = [('epsa', 'year'), ]
    for i in range(51):
        fields_list.append((f'v{i+1}', f'v{i+1}_type'))
    fields = tuple(fields_list)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS - Seguimiento Regulatorio: Reportes de Variables'}
        return super(VariableReportModelAdmin, self).changelist_view(request, extra_context=extra_context)

@admin.register(models.IndicatorMeasurement)
class IndicatorMeasurementModelAdmin(admin.ModelAdmin):
    view_on_site = False
    list_filter = ('year', 'month', 'epsa')
    search_fields = ['epsa', 'year',]
    list_display = ('epsa', 'year', 'month', 'get_category', 'get_state',)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS - Seguimiento Regulatorio: Medidas de Indicadores'}
        return super(IndicatorMeasurementModelAdmin, self).changelist_view(request, extra_context=extra_context)



