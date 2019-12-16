from django.contrib import admin
from planning import models


class PlanGoalInline(admin.TabularInline):
    model = models.PlanGoal
    verbose_name = 'Meta'
    verbose_name_plural = 'Metas'

class CoopExpenseInline(admin.StackedInline):
    model = models.CoopExpense

class MuniExpenseInline(admin.StackedInline):
    model = models.MuniExpense

@admin.register(models.POA)
class POAModelAdmin(admin.ModelAdmin):
    view_on_site = False

    inlines = [CoopExpenseInline, MuniExpenseInline]
    
    list_filter = ('epsa','year',)
    search_fields = ['epsa', 'year',]
    list_display = ('epsa', 'year', 'order', 'get_category', 'get_state',)

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS - Planificación: POAs'}
        return super(POAModelAdmin, self).changelist_view(request, extra_context=extra_context)

    fieldsets = (
        ('General',{'fields':('epsa','year','order',)}),
        ('Ingresos',{'fields':('in_op_ap','in_op_alc','in_op_alc_pozo','in_op_otros','in_financieros','in_no_op_otros',)}),
        ('Inversiones',{'fields':('inv_infraestructura_ap','inv_infraestructura_alc','inv_equipo','inv_diseno_estudio','inv_otros')}),
        ('Metas de Expansión',{'fields':('pob_total','pob_ap','pob_alc','con_ap','con_ap_total','cob_ap','con_alc','con_alc_total','cob_alc','cob_micro','anc',)}),
    )


@admin.register(models.Plan)
class PlanModelAdmin(admin.ModelAdmin):
    view_on_site = False
    inlines = [
        PlanGoalInline,
    ]
    
    list_display = ('epsa', 'year', 'plan_type', 'get_category', 'get_state',)
    list_filter = ('epsa','year')
    search_fields = ['epsa', 'year',]

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS - Planificación: PDQs/PTDS'}
        return super(PlanModelAdmin, self).changelist_view(request, extra_context=extra_context)


