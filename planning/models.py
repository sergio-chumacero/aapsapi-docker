import datetime
from django.db import models
from performance.models import EPSA, BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError

state_code_to_name = {
    'LP': 'La Paz',
    'CO': 'Cochabamba',
    'PO': 'Potosí',
    'SC': 'Santa Cruz',
    'CH': 'Chuquisaca',
    'OR': 'Oruro',
    'TA': 'Tarija',
    'BE': 'Beni',
    'PA': 'Pando',
}

class POA(BaseModel):
    '''
    Modelo representando un Presupuesto Operativo Anual (POA) de una EPSA.
    '''
    epsa = models.CharField(
        max_length=64,
        verbose_name='EPSA',
        help_text='EPSA que reporta el POA'
    )
    year = models.IntegerField(
        verbose_name='Año',
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1900)],
        help_text='Año del POA'
    )
    order = models.IntegerField(
        verbose_name='Orden',
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Orden del POA (inicial:1, reprogramado:2-5)'
    )

    in_op_ap = models.FloatField(
        verbose_name=f'ingresos por servicios de agua potable',
        help_text= f'Ingresos por servicios de agua potable. (Bs.)',
        blank='True',
        null='True',
    )

    in_op_alc = models.FloatField(
        verbose_name=f'ingresos por servicios de alcantarillado',
        help_text= f'Ingresos por servicios de alcantarillado sanitario. (Bs.)',
        blank='True',
        null='True',
    )

    in_op_alc_pozo = models.FloatField(
        verbose_name=f'ingresos por servicios de alcantarillado de pozo',
        help_text= f'Ingresos por servicios de alcantarillado de pozo',
        blank='True',
        null='True',
    )

    in_op_otros = models.FloatField(
        verbose_name=f'otros ingresos operativos',
        help_text= f'Ingresos por otro tipo de servicios operativos. (Bs.)',
        blank='True',
        null='True',
    )

    in_financieros = models.FloatField(
        verbose_name=f'ingresos financieros',
        help_text= f'Ingresos no operativos financieros. (Bs.)',
        blank='True',
        null='True',
    )

    in_no_op_otros = models.FloatField(
        verbose_name=f'otros ingresos no operativos',
        help_text= f'Otros ingresos no operativos. (Bs.)',
        blank='True',
        null='True',
    )

    inv_infraestructura_ap = models.FloatField(
        verbose_name=f'inversiones de infraestructura de agua potable',
        help_text= f'Inversiones para la construcción de infraestructura de agua potable. (Bs.)',
        blank='True',
        null='True',
    )

    inv_infraestructura_alc = models.FloatField(
        verbose_name=f'inversiones de infraestructura de alcantarillado',
        help_text= f'Inversiones para la construcción de infraestructura de alcantarillado sanitario. (Bs.)',
        blank='True',
        null='True',
    )

    inv_equipo = models.FloatField(
        verbose_name=f'inversiones de maquinaria y equipo',
        help_text= f'Inversiones para la adquisición de maquinaria y equipo. (Bs.)',
        blank='True',
        null='True',
    )

    inv_diseno_estudio = models.FloatField(
        verbose_name=f'inversiones de diseño y estudio de proyectos',
        help_text= f'Inversiones para el diseño y estudio de proyectos. (Bs.)',
        blank='True',
        null='True',
    )
    
    inv_otros = models.FloatField(
        verbose_name=f'inversiones de infraestructura de agua potable',
        help_text= f'Inversiones por construcción de infraestructura de agua potable. (Bs.)',
        blank='True',
        null='True',
    )

    # Metas de Expansión

    pob_total = models.FloatField(
        verbose_name=f'población total',
        help_text= f'Población Total (hab.)',
        blank='True',
        null='True',
    )

    pob_ap = models.FloatField(
        verbose_name=f'población con agua potable',
        help_text= f'Población con Agua Potable (hab.)',
        blank='True',
        null='True',
    )
    pob_alc = models.FloatField(
        verbose_name=f'población con alcantarillado',
        help_text= f'Población con Alcantarillado (hab.)',
        blank='True',
        null='True',
    )
    con_ap = models.FloatField(
        verbose_name=f'conexiones AP nuevas',
        help_text= f'Conexiones Nuevas de Agua Potable (N°)',
        blank='True',
        null='True',
    )
    con_ap_total = models.FloatField(
        verbose_name=f'total conexiones AP',
        help_text= f'Total de Conexiones de Agua Potable (N°)',
        blank='True',
        null='True',
    )
    cob_ap = models.FloatField(
        verbose_name=f'cobertura AP',
        help_text= f'Cobertura de Agua Potable(%)',
        blank='True',
        null='True',
    )
    con_alc = models.FloatField(
        verbose_name=f'conexiones de alcantarillado nuevas',
        help_text= f'Nuevas Conexiones de Alcantarillado (N°)',
        blank='True',
        null='True',
    )
    con_alc_total = models.FloatField(
        verbose_name=f'total conexiones de alcantarillado',
        help_text= f'Total de Conexiones de Alcantarillado (N°)',
        blank='True',
        null='True',
    )
    cob_alc = models.FloatField(
        verbose_name=f'cobertura de alcantarillado',
        help_text= f'Cobertura de Alcantarillado (%)',
        blank='True',
        null='True',
    )
    cob_micro = models.FloatField(
        verbose_name=f'cobertura de micromedición',
        help_text= f'Cobertura de Micromedición (%)',
        blank='True',
        null='True',
    )
    anc = models.FloatField(
        verbose_name=f'agua no contabilizada',
        help_text= f'Índice de Agua No Contabilizada (%)',
        blank='True',
        null='True',
    )
    
    class Meta:
        unique_together = ('epsa','year','order',)
        verbose_name = 'POA'
        verbose_name_plural = 'POAs'
        ordering = ['epsa','year','order',]

    def clean(self, *args, **kwargs):
        if hasattr(self, 'coop_expense') and hasattr(self, 'muni_expense'):
            raise ValidationError('Un POA no puede tener más de un tipo de planilla de gastos (cooperativa, municipal, ...).', code='invalid')
        super(POA, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(POA, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.epsa}-{self.year}-{self.order}'
    def get_category(self):
        rel_epsa = EPSA.objects.filter(code=self.epsa)
        if rel_epsa:
            cat = str(rel_epsa[0].category)
            if cat in ['A','B','C','D']:
                return cat
        return ''
    get_category.short_description = 'categoría'
    def get_state(self):
        rel_epsa = EPSA.objects.filter(code=self.epsa)
        if rel_epsa:
            state_code = str(rel_epsa[0].state)
            if state_code in state_code_to_name.keys():
                return state_code_to_name[state_code]
        return ''
    get_state.short_description = 'departamento'


class CoopExpense(BaseModel):
    '''
    Modelo representando los gastos de una cooperativa correspondiente a un POA.
    '''
    poa = models.OneToOneField(
        to=POA,
        on_delete=models.CASCADE,
        related_name='coop_expense',
        verbose_name='poa',
        help_text='POA al cual corresponden los gastos.'
    )
    costos_operacion = models.FloatField(
        verbose_name=f'costos de operación',
        help_text= f'Costos de operación. (Bs.)',
        blank='True',
        null='True',
    )
    costos_mantenimiento = models.FloatField(
        verbose_name=f'costos de mantenimiento',
        help_text= f'Costos de mantenimiento. (Bs.)',
        blank='True',
        null='True',
    )
    gastos_administrativos = models.FloatField(
        verbose_name=f'gastos administrativos',
        help_text= f'Gastos administrativos. (Bs.)',
        blank='True',
        null='True',
    )
    gastos_comerciales = models.FloatField(
        verbose_name=f'gastos comerciales',
        help_text= f'Gastos comerciales. (Bs.)',
        blank='True',
        null='True',
    )
    gastos_financieros = models.FloatField(
        verbose_name=f'gastos financieros',
        help_text= f'Gastos financieros. (Bs.)',
        blank='True',
        null='True',
    )
    class Meta:
        verbose_name = 'Planilla de gastos POA de cooperativa'
        verbose_name_plural = 'Planillas de gastos POA de cooperativa'
        ordering = ['poa', 'id',]

    def __str__(self):
        return f'{self.poa} ({self.id})'

class MuniExpense(BaseModel):
    '''
    Modelo representando los gastos de una EPSA municipal correspondiente a un POA.
    '''
    poa = models.OneToOneField(
        to=POA,
        on_delete=models.CASCADE,
        related_name='muni_expense',
        verbose_name='poa',
        help_text='POA al cual corresponden los gastos.'
    )
    gastos_empleados_permanentes = models.FloatField(
        verbose_name=f'empleados permanentes',
        help_text= f'Gastos relacionados a empleados permanentes. (Bs.)',
        blank='True',
        null='True',
    )
    gastos_empleados_no_permanentes = models.FloatField(
        verbose_name=f'empleados no permanentes',
        help_text= f'Gastos relacionados a empleados no permanentes. (Bs.)',
        blank='True',
        null='True',
    )
    gastos_prevision_social = models.FloatField(
        verbose_name=f'previsión social',
        help_text= f'Gastos relacionados a previsión social. (Bs.)',
        blank='True',
        null='True',
    )
    gastos_servicio_no_personales = models.FloatField(
        verbose_name=f'servicio no personales',
        help_text= f'Gastos relacionados a servicios no personales. (Bs.)',
        blank='True',
        null='True',
    )
    gastos_materiales = models.FloatField(
        verbose_name=f'materiales y suministros',
        help_text= f'Gastos relacionados a materiales y suministros. (Bs.)',
        blank='True',
        null='True',
    )
    gastos_activos = models.FloatField(
        verbose_name=f'activos reales',
        help_text= f'Gastos relacionados a activos reales. (Bs.)',
        blank='True',
        null='True',
    ) 
    gastos_deuda_publica = models.FloatField(
        verbose_name=f'servicio de la deuda pública',
        help_text= f'Gastos relacionados al servicio de la deuda pública. (Bs.)',
        blank='True',
        null='True',
    )
    gastos_transferencias = models.FloatField(
        verbose_name=f'transferencias',
        help_text= f'Gastos relacionados a tranferencias (Bs.)',
        blank='True',
        null='True',
    )
    gastos_impuesto = models.FloatField(
        verbose_name=f'impuestos, regalías y tasas',
        help_text= f'Gastos relacionados a impuestos, regalías y tasas. (Bs.)',
        blank='True',
        null='True',
    )
    gastos_otros = models.FloatField(
        verbose_name=f'otros gastos',
        help_text= f'Otros gastos. (Bs.)',
        blank='True',
        null='True',
    )
    class Meta:
        verbose_name = 'Planilla de gastos POA de EPSA municipal'
        verbose_name_plural = 'Planillas de gastos POA de EPSA municipal'
        ordering = ['poa', 'id',]

    def __str__(self):
        return f'{self.poa} ({self.id})'

class Plan(BaseModel):
    '''
    Modelo representando un plan de desarrollo quinquenal (PDQ) o un plan transitorio de desarrollo sostenible (PTDS).
    '''
    PLAN_TYPES = (
        ('pdq', 'PDQ'),
        ('ptds', 'PTDS'),
    )

    epsa = models.CharField(
        max_length=64,
        verbose_name='EPSA',
        help_text='EPSA que reporta el PTDS'
    )
    year = models.IntegerField(
        verbose_name='Año Inicial',
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1900)],
        help_text='Primer año de vigencia del PTDS'
    )
    plan_type = models.CharField(
        verbose_name= 'tipo de plan',
        max_length= 8,
        choices= PLAN_TYPES,
        default='pdq',
        help_text= 'Tipo del plan (PDQ o PTDS).', 
    )  
    class Meta:
        unique_together = ('epsa','year')
        verbose_name = 'PDQ/PTDS'
        verbose_name_plural = 'PDQs/PTDS'
        ordering = ['epsa','year',]

    def __str__(self):
        return f'{self.epsa}-{self.year}-{self.plan_type}'
    def get_category(self):
        rel_epsa = EPSA.objects.filter(code=self.epsa)
        if rel_epsa:
            cat = str(rel_epsa[0].category)
            if cat in ['A','B','C','D']:
                return cat
        return ''
    get_category.short_description = 'categoría'
    def get_state(self):
        rel_epsa = EPSA.objects.filter(code=self.epsa)
        if rel_epsa:
            state_code = str(rel_epsa[0].state)
            if state_code in state_code_to_name.keys():
                return state_code_to_name[state_code]
        return ''
    get_state.short_description = 'departamento'


class PlanGoal(BaseModel):
    '''
    Modelo representando una meta de expansión de un PDQ o PTDS.
    '''
    plan = models.ForeignKey(
        to= Plan,
        verbose_name= 'PDQ/PTDS',
        on_delete=models.CASCADE,
        related_name='goals',
        help_text='PDQ/PTDS al cual pertenece la meta.',  
    )
    year = models.IntegerField(
        verbose_name='año',
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1900)],
        help_text='año del plan'
    )
    description = models.CharField(
        verbose_name= 'descripción',
        max_length= 256,
        help_text= 'Descripción de la meta.'
    )
    value = models.FloatField(
        verbose_name=f'valor',
        help_text= f'Valor de la meta.'
    )
    val_description = models.CharField(
        verbose_name='descripción del valor',
        max_length=64,
        help_text='Descripción de lo que representa el valor de la meta (ejemplo: más de X conexiones nuevas de agua potable o simplemente ">").',
        blank=True, null=True,
    )
    unit = models.CharField(
        verbose_name= 'unidad',
        max_length= 64,
        help_text= 'Unidad de la meta.'
    )
    class Meta:
        verbose_name = 'Meta de expansión PDQ/PTDS'
        verbose_name_plural = 'Metas de expansión PDQ/PTDS'
        ordering = ['plan', 'id',]

    def __str__(self):
        return f'{self.plan} ({self.id})'