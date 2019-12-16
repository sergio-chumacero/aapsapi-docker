from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class BaseModel(models.Model):
    '''
    Abstract Django Model that adds a `modified` field to all Models, allowing for smart caching at the client side. 
    '''
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

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


class EPSA(BaseModel):
    '''
    Modelo representando una EPSA (Entidad Prestadora de Servicios de Agua Potable y Saneamiento).
    '''
    STATE_CHOICES = (
        ('LP', 'La Paz'),
        ('CO', 'Cochabamba'),
        ('PO', 'Potosí'),
        ('SC', 'Santa Cruz'),
        ('CH', 'Chuquisaca'),
        ('OR', 'Oruro'),
        ('TA', 'Tarija'),
        ('BE', 'Beni'),
        ('PA', 'Pando'),
    )
    CATEGORY_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    code = models.CharField(
        max_length=64,
        primary_key=True,
        verbose_name='sigla',
        help_text='Sigla de la EPSA. Debe ser único y contener no más de 16 caracteres. De preferencia en mayúsculas. Campo obligatorio.',
    )
    name = models.CharField(
        max_length=255, 
        blank=True,
        null=True,
        verbose_name='nombre',
        help_text='Nombre de la EPSA.'
    )
    state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        blank=True,
        null=True,
        verbose_name='departamento',
        help_text='Departamento de la EPSA.'
    )
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True,
        verbose_name='categoría',
        help_text='Categoría de la EPSA.')

    class Meta:
        verbose_name = 'EPSA'
        verbose_name_plural = 'EPSAs'
        ordering = ['category', 'code', ]

    def __str__(self):
        return self.code

class Variable(BaseModel):
    '''
    Modelo representando una Variable.
    '''
    TYPE_CHOICES = (
        ('volumen', 'Volumen'),
        ('capacidad', 'Capacidad'),
        ('muestras_calidad', 'Muestras para Calidad'),
        ('conexiones', 'Conexiones'),
        ('poblacion', 'Población'),
        ('abastecimiento', 'Abastecimiento'),
        ('balance_general', 'Balance General'),
        ('estado_resultados', 'Estado de Resultados'),
        ('inversiones', 'Inversiones'),
        ('personal', 'Personal'),
        ('reclamos', 'Reclamos'),
        ('muestras_presion', 'Muestras de Presión'),
        ('fallas', 'Fallas'),
    )
    code = models.CharField(
        max_length=32,
        primary_key=True,
        verbose_name='código',
        help_text='Código de variable. Debe ser único y contener no más de 16 caracteres.',
    )
    var_id = models.PositiveSmallIntegerField(
        verbose_name='Número de Variable',
        unique=True,
        help_text='Número identificatorio de la variable. Único.'
    )
    name = models.CharField(
        max_length=255, 
        blank=True,null=True,
        verbose_name='nombre',
        help_text='Nombre completo de la variable.'
    )
    unit = models.CharField(verbose_name='unidad',
        max_length=16,
        blank=True, null=True,
        help_text='Unidad de medida de la variable.'
    )
    var_type = models.CharField(
        verbose_name='Tipo de Variable',
        max_length=32,
        choices=TYPE_CHOICES,
        blank=True, null=True,
        help_text='El tipo de la variable.'
    )
    class Meta:
        verbose_name = 'Variable'
        verbose_name_plural = 'Variables'
        ordering = ['var_id',]
    def __str__(self):
        return self.code

class Indicator(BaseModel):
    '''
    Modelo representando un Indicador.
    '''
    CRITERIA_TYPES = (
        ('Confiabilidad del recurso hídrico',
         (('disponibilidad_recurso', 'Disponibiidad del recurso'),
          ('calidad_recurso', 'Calidad del recurso'))),
        ('Estabilidad de abstecimiento',
         (('abastecimiento', 'Abastecimiento Continuo'),
          ('alcanse', 'Alcanse de los servicios'))),
        ('Protección al medio ambiente',
         (('sostenibilidad_sub', 'Explotación sostenible acuíferos subterráneos'),
          ('contaminacion', 'Contaminación por aguas residuales'))),
        ('Manejo apropiado del sistema de agua potable y alcantarillado sanitario',
         (('manejo_apropiado_mejora', 'Mejora continua del servicio en base a las necesidades de los usuarios'),
          ('mantenimiento', 'Mantenimiento Apropiado'))),
        ('Sostenibilidad económica y administrativa del servicio',
         (('razonabilidad_economica', 'Razonabilidad económica para la prestación del servicio'),
          ('sostenibilidad_mejora', 'Mejora continua del servicio en base a las necesidades de los usuarios'))),
    )
    code = models.CharField(
        max_length=32,
        primary_key = True,
        verbose_name='código',
        help_text='Código del indicador. Debe ser único y contener no más de 16 caracteres.',
    )
    ind_id = models.PositiveSmallIntegerField(
        verbose_name='Número de Variable',
        unique=True,
        help_text='Número identificatorio de la variable. Único.'
    )
    name = models.CharField(
        max_length=255, 
        blank=True,
        null=True,
        verbose_name='nombre',
        help_text='Nombre del indicador.'
    )
    unit = models.CharField(
        verbose_name='unidad',
        max_length=32,
        blank=True, null=True,
        help_text='Unidad de medida del indicador.'
    )
    criteria = models.CharField(
        verbose_name='objetivo-critério',
        max_length=32,
        blank=True, null=True,
        choices=CRITERIA_TYPES,
        help_text='Objetivo/Critério del indicador.'
    )
    # formula = JSONField(
    #     blank=True, null=True,
    #     help_text='Formula para calcular el indicador en formato JsonLogic.'
    # )
    class Meta:
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'
        ordering = ['ind_id',]
    def __str__(self):
        return self.code

for m, m0 in zip(['min', 'max'], ['mínimo', 'máximo']):
    for cat in ['A', 'B', 'C', 'D']:
        Indicator.add_to_class(
            f'par_{m}_{cat}',
            models.FloatField(
                verbose_name=f'parametro {m0} {cat}',
                blank=True, null=True,
                help_text=f'Parámetro {m}. para la categoría {cat}.'
            )
        )

class VariableReport(BaseModel):
    '''
    Modelo representando un reporte mensual, semestral o anual completo de variables.
    '''
    epsa = models.CharField(
        max_length=64,
        verbose_name='EPSA',
        help_text='EPSA que reporta las variables',
        blank=True, null=True,
    )
    year = models.IntegerField(
        verbose_name='Año',
        default=datetime.now().year,
        help_text='Año de reporte',
        validators=[MinValueValidator(1900)]
    )
    month = models.IntegerField(
        verbose_name='mes',
        help_text='Mes del reporte o blanco si el reporte es anual.',
        blank=True, null=True,
        default=1,
        validators=[MinValueValidator(1),MaxValueValidator(12)]
    )
    class Meta:
        unique_together=('epsa','year','month')
        verbose_name = 'Reporte de variables'
        verbose_name_plural = 'Reportes de variables'
        ordering = ['epsa', 'year','month']
    def __str__(self):
        m = '-' + str(self.month) if self.month else ''
        return f'{str(self.epsa)}-{str(self.year)}{m}'
    def get_category(self):
        rel_epsa = EPSA.objects.filter(code=self.epsa)
        if rel_epsa:
            cat = rel_epsa[0].category
            if str(cat) in ['A','B','C','D']:
                return str(cat)
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

VARIABLE_TYPE_CHOICES = (
    ('VA', 'valor'),
    ('NC', 'NC: No Corresponde'),
    ('NR', 'NR: No Reportó'),
    ('NB', 'NB: Norma Boliviana'),
    ('MS', 'MS: Manual de Seguimiento'),
)
VAR_VNAMES = [
    'Volumen de agua cruda extraído de la(s) fuente(s) superficial(es)',
    'Volumen de agua cruda extraído de la(s) fuente(s) subterránea(s) ',
    'Volumen de agua potable producido (Planta de tratamiento y/o tanque de desinfección)',
    'Volumen de agua potable tratada en planta de tratamiento',
    'Volumen de agua potable facturado',
    'Volumen tratado de agua residual',
    'Capacidad autorizada de captación de la(s) fuente(s) de agua cruda',
    'Capacidad máxima de agua actual de la fuente subterránea',
    'Capacidad instalada de la planta de tratamiento de agua potable',
    'Capacidad instalada de la planta de tratamiento de agua residual',
    'Número de muestras ejecutadas de agua potable',
    'Número de muestras recomendadas de agua potable',
    'Número de análisis satisfactorios de agua potable',
    'Número de análisis ejecutados de agua potable',
    'Número de análisis satisfactorios de agua residual tratada',
    'Número de análisis ejecutados de agua residual tratada',
    'Número total de conexiones de agua potable activas medidas y no medidas',
    'Número total de conexiones de alcantarillado sanitario activas ',
    'Número total de medidores de agua potable instalados ',
    'Habitantes por conexión de agua potable (Población abastecida)',
    'Habitantes por conexión de alcantarillado sanitario (Población servida)',
    'Población total (Del área de servicio autorizado)',
    'Población abastecida',
    'Población servida', 'Horas periodo analizado', 'Horas periodo analizado',
    'Sumatoria ponderada de horas por usuario afectados por racionamiento',
    'Sumatoria ponderada de horas por usuario afectados por corte',
    'Activo disponible',
    'Cuentas por cobrar de facturación gestión actual',
    'Activo total', 'Pasivo corriente',
    'Pasivo no corriente', 'Ingresos operativos del servicio',
    'Ingresos por servicios', 'Costos operativos del servicio',
    'Costos operativos totales',
    'Inversiones ejecutadas',
    'Inversiones presupuestadas',
    'Número de empleados técnicos y/o profesionales',
    'Total personal',
    'Número de reclamos atendidos',
    'Número de reclamos presentados',
    'Número de puntos con presión dentro el rango aceptable según NB o MS',
    'Número total de puntos de muestreo de presión',
    'Número de fallas en tubería de red de agua potable',
    'Número de fallas en conexiones de agua potable',
    'Longitud total de red de agua potable ',
    'Número de fallas en tubería de red de alcantarillado sanitario',
    'Número de fallas en conexiones de alcantarillado sanitario',
    'Longitud total de red de alcantarillado sanitario'
]

VAR_HTEXTS = [
    'm3/periodo', 'm3/periodo', 'm3/periodo', 'm3/periodo', 'm3/periodo', 'm3/periodo',
    'm3/hrs', 'm3/hrs', 'm3/hrs', 'm3/hrs',
    'muestras', 'muestras',
    'análisis', 'análisis', 'análisis', 'análisis',
    'conex.', 'conex.',
    'medidores',
    'hab /conex.', 'hab /conex.',
    'hab.', 'hab.', 'hab.',
    'hrs/día', 'hrs/periodo',
    'hrs x conex.', 'hrs x conex.',
    'Bs.', 'Bs.', 'Bs.', 'Bs.', 'Bs.', 'Bs.', 'Bs.', 'Bs.', 'Bs.', 'Bs.', 'Bs.',
    'empleados', 'empleados',
    'reclamos', 'reclamos',
    'puntos', 'puntos',
    'fallas', 'fallas',
    'km.', 'fallas', 'fallas', 'km.'
]

for i, var_vname, var_htext in zip(range(51), VAR_VNAMES, VAR_HTEXTS):
    VariableReport.add_to_class(
        f'v{i+1}',
        models.FloatField(
            verbose_name=f'{i+1}.-' + var_vname,
            blank=True, null=True,
            help_text= var_vname + f'(unidad: {var_htext})'
        )
    )
    VariableReport.add_to_class(
        f'v{i+1}_type',
        models.CharField(verbose_name='Tipo de dato',
        max_length=2,
        choices=VARIABLE_TYPE_CHOICES,
        default='VA', 
        help_text=f'Tipo de la variable {i} reportada.'
        )
    )


class IndicatorMeasurement(BaseModel):
    '''
    Modelo Representando la medida de un Indicador en base a un reporte mensual, semestral o anual.
    '''
    epsa = models.CharField(
        max_length=64,
        verbose_name='EPSA',
        help_text='EPSA que reporta las variables',
        blank=True, null=True,
    )
    year = models.IntegerField(
        verbose_name='año',
        default=datetime.now().year,
        help_text='Año del reporte.',
        validators=[MinValueValidator(1900)]
    )
    month = models.IntegerField(
        verbose_name='mes',
        help_text='Mes del reporte o blanco si el reporte es anual.',
        blank=True, null=True,
        default=1,
        validators=[MinValueValidator(1),MaxValueValidator(12)]
    )
    class Meta:
        unique_together = ('epsa','year','month',)
        verbose_name = 'Medida de indicadores'
        verbose_name_plural = 'Medidas de indicadores'
        ordering = ['epsa', 'year','month']
    def __str__(self):
        return f'{self.epsa}-{self.year}'
    def get_category(self):
        rel_epsa = EPSA.objects.filter(code=self.epsa)
        if rel_epsa:
            cat = rel_epsa[0].category
            if str(cat) in ['A','B','C','D']:
                return str(cat)
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

INDICATOR_NAMES = ['Rendimiento actual de la fuente', 'Uso eficiente del recurso', 'Cobertura de muestras de agua potable', 'Conformidad de los análisis de agua potable realizados', 'Dotación', 'Continuidad por racionamiento', 'Continuidad por corte', 'Cobertura del servicio de agua potable', 'Cobertura del servicio de alcantarillado sanitario', 'Cobertura de micromedición', 'Incidencia extracción de agua cruda subterránea ', 'Índice de tratamiento de agua residual', 'Control de agua residual', 'Capacidad instalada de planta de tratamiento de agua potable', 'Capacidad instalada de planta de tratamiento de agua residual ',
                   'Presión del servicio de agua potable', 'Índice de agua no contabilizada en producción', 'Índice de agua no contabilizada en la red', 'Densidad de fallas en tuberías de agua potable', 'Densidad de fallas en conexiones de agua potable', 'Densidad de fallas en tuberías de agua residual', 'Densidad de fallas en conexiones de agua residual', 'Índice de operación eficiente', 'Prueba ácida', 'Eficiencia de recaudación', 'Índice de endeudamiento total', 'Tarifa media', 'Costo unitario de operación', 'Índice de ejecución de inversiones', 'Personal calificado', 'Número de empleados por cada 1000 conexiones', 'Atención de reclamos']
INDICATOR_UNITS = ['%', '%', '%', '%', 'l/hab/día', 'hr/día', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', 'fallas/100km',
                   'fallas/1000conex.', 'fallas/100km', 'fallas/1000conex.', '%', '-', '%', '%', '%CUO(Bs.)', '%TM(Bs.)', '%', '%', 'empleados/1000conex.', '%']
for i, ind_name, ind_unit in zip(range(32), INDICATOR_NAMES, INDICATOR_UNITS):
    IndicatorMeasurement.add_to_class(
        f'ind{i+1}',
        models.FloatField(
            verbose_name=f'{i+1}.- ' + ind_name,
            blank=True, null=True,
            help_text=ind_name + f'(unidad: {ind_unit})'
        )
    )


