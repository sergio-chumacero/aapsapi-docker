from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from djgeojson.fields import PointField
from performance.models import EPSA

state_code_to_name = dict(
    LP='La Paz',
    CO='Cochabamba',
    PO='Potosí',
    SC='Santa Cruz',
    CH='Chuquisaca',
    OR='Oruro',
    TA='Tarija',
    BE='Beni',
    PA='Pando',
)

class SARH(models.Model):
    '''
    Modelo representando un Sistema de Autoabastecimiento de Recursos Hídricos (SARH).
    ''' 
    AIS_CHOICES = (
        ('ACTIVO', 'ACTIVO'),
        ('INACTIVO', 'INACTIVO'),
        ('SELLADO', 'SELLADO')
    )
    SUB_SUP_CHOICES = (
        ('SUBTERRANEO','SUBTERRANEO'),
        ('SUPERFICIAL','SUPERFICIAL'),
    )
    REG_RENOV_CHOICES = (
        ('REG','REG'),
        ('RENOV','RENOV'),
    )
    AUTH_STATE_CHOICES = (
        ('VIGENTE','VIGENTE'),
        ('VENCIDO','VENCIDO'),
        ('SELLADO','SELLADO'),
    )
    STATE_CHOICES = (
        ('LA PAZ', 'LA PAZ'),
        ('COCHABAMBA', 'COCHABAMBA'),
        ('POTOSI', 'POTOSI'),
        ('SANTA CRUZ', 'SANTA CRUZ'),
        ('CHUQUISACA', 'CHUQUISACA'),
        ('ORURO', 'ORURO'),
        ('TARIJA', 'TARIJA'),
        ('BENI', 'BENI'),
        ('PANDO', 'PANDO'),
    )
    DISCHARGE_CHOICES = (
        ('S.A.S.', 'S.A.S.'),
        ('RED DE ALCANTARILLADO', 'RED DE ALCANTARILLADO'),
        ('CUERPO RECEPTOR', 'CUERPO RECEPTOR'),
        ('NO DESCARGA', 'NO DESCARGA'),
    )

    sarh_id = models.CharField(
        primary_key = True,
        max_length = 32,
        verbose_name = 'id del SARH',
        help_text = 'Llave primaria (ID) del SARH. Creado en base al número de fuente. No debe contenter más de 32 caracteres. De preferencia en formato "XXXXX-XXXXX-X". Campo obligatorio.'
    )

    folder_code	= models.CharField(
        max_length=16,
        verbose_name='código de carpeta',
        help_text='Código de la carpeta del SARH. No debe contener más de 16 caracteres. De preferencia en mayúsculas.',
        blank=True,null=True,
    )
    epsa = models.CharField(
        max_length=64,
        help_text='EPSA que provee el servicio SARH.',
        blank=True, null=True,
    )
    user = models.CharField(
        max_length=254,
        verbose_name='usuario del sarh',
        help_text='Usuario del servicio SARH. No debe contener más de 254 caracteres. De preferencia en mayúsculas.',
        blank=True,null=True,
    )
    sub_subt = models.CharField(
        max_length=16,
        choices=SUB_SUP_CHOICES,
        verbose_name='subterraneo/superficial',
        help_text='Tipo de SARH (Subterráneo/Superficial).',
        blank=True, null=True,
    )
    reg_renov = models.CharField(
        max_length=8,
        choices=REG_RENOV_CHOICES,
        verbose_name='reg./renov.',
        help_text='Regularización o Renovación',
        blank=True, null=True,
    )
    rar_aaps_nr = models.CharField(
        max_length=16,
        verbose_name='número RAR/AAPS',
        help_text='Número de registro RAR/AAPS.',
        blank=True, null=True,
    )
    rar_date = models.DateField(
        verbose_name='fecha de la RAR',
        help_text='Fecha de la RAR. Debe estar en formato "aaaa-mm-dd".',
        blank=True, null=True,
    )	
    notification_date = models.DateField(
        verbose_name='fecha de emisión de notificación a la EPSA.',
        blank=True,null=True,
        help_text='Fecha de Emisión de la Notificación a la EPSA. Debe estar en formato "aaaa-mm-dd".'
    )		
    user_notification_date = models.DateField(
        verbose_name='fecha de notificación de la EPSA al usuario',
        blank=True,null=True,
        help_text='Fecha de notificación de la EPSA al usuario. Debe estar en formato "aaaa-mm-dd".'
    )	
    auth_year =	models.IntegerField(
        verbose_name='año de autorización',
        default=datetime.now().year,
        help_text='Año de Autorización. Debe ser un número entero mayor o igual a 1800.',
        validators=[MinValueValidator(1800)],
        blank=True, null=True,
    )
    renovation_alert = models.IntegerField(
        verbose_name='alerta de renovación',
        default=datetime.now().year,
        blank=True,null=True,
        help_text='Alerta de Renovación.',
    )
    auth_certificate_state = models.CharField(
        max_length=32,
        choices=AUTH_STATE_CHOICES,
        verbose_name='estado del certificado de autorización',
        help_text='Estado del certificado de autorización (VIGENTE,VENCIDO o SELLADO).',
        blank=True, null=True,
    )
    state = models.CharField(
        max_length=32,
        choices=STATE_CHOICES,
        blank=True, null=True,
        verbose_name='departamento',
        help_text='Departamento del SARH.'
    )
    municipality = models.CharField(
        max_length=128,
        blank=True, null=True,
        verbose_name='miunicipio',
        help_text='Municipio del SARH. No debe contener más de 128 caracteres.'
    )	
    industry_type =	models.CharField(
        max_length=256,
        blank=True, null=True,
        verbose_name='rubro',
        help_text='Rubro de uso del SARH. No debe contener más de 256 caracteres.'
    )
    use_description = models.CharField(
        max_length=512,
        blank=True, null=True,
        verbose_name='descripción de uso',
        help_text='Descripción de uso del SARH. No debe contener más de 512 caracteres.'
    )
    form_extraction_volume = models.FloatField(
        verbose_name=f'Volumen de extracción del formulario único',
        blank=True, null=True,
        help_text=f'Volumen de Extracción del Formulario Único (m3/mes).'
    )
    authorized_streamflow = models.FloatField(
        verbose_name=f'caudal de extracción autorizado en RAR',
        blank=True, null=True,
        help_text=f'Caudal de Extracción Autorizado en RAR. (l/s).'
    ) 
    anual_volume = models.FloatField(
        verbose_name=f'volumen explotado reportado anualmente',
        blank=True, null=True,
        help_text=f'Volumen Explotado Reportado Anualmente. (m3/mes).'
    )  	
    sarh_denom = models.CharField(
        max_length=512,
        verbose_name=f'denominación del SARH',
        blank=True, null=True,
        help_text=f'denominación del SARH. (m3/mes). No debe contener más de 512 caracteres.'
    )  	 
    active_inactive_sealed = models.CharField(
        max_length=16,
        choices=AIS_CHOICES,
        verbose_name='activo/inactivo/sellado',
        help_text='Condición Actual del SARH (ACTIVO, INACTIVO o SELLADO).',
        blank=True, null=True,
    )
    x = models.FloatField(
        verbose_name='coordenada x (utm)',
        help_text='Coordenada x en sistema UTM.',
        blank=True,null=True,
    )
    y = models.FloatField(
        verbose_name='coordenada y (utm)',
        help_text='Coordenada x en sistema UTM.',
        blank=True,null=True,
    )
    z = models.FloatField(
        verbose_name='coordenada z (utm)',
        help_text='Coordenada x en sistema UTM.',
        blank=True,null=True,
    )
    zone = models.CharField(
        max_length=8,
        verbose_name='zona de coordenadas (utm)',
        help_text='Zona de coordenadas UTM.',
        blank=True,null=True,
    )
    source_nr = models.CharField(
        max_length=32,
        verbose_name=f'número de fuente',
        help_text=f'Número de Fuente. No debe contener más de 32 caracteres.',
        blank=True, null=True,
    ) 		
    discharge_place = models.CharField(
        max_length=56,
        choices=DISCHARGE_CHOICES,
        verbose_name=f'lugar de descarga',
        help_text=f'Lugar de descarga de Aguas Residuales.',
        blank=True, null=True,
    )	 	
    ph = models.FloatField(
        verbose_name='ph',
        blank=True, null=True,
        help_text=f'PH.'
    )  	
    conductivity = models.FloatField(
        verbose_name=f'conductividad',
        blank=True, null=True,
        help_text=f'Conductividad (µS/cm).'
    )  		
    turbidity = models.FloatField(
        verbose_name=f'turbidad',
        blank=True, null=True,
        help_text=f'Turbiedad (MTU).'
    )  		
    iron = models.FloatField(
        verbose_name=f'hierro',
        blank=True, null=True,
        help_text=f'Hierro'
    )  		
    manganese = models.FloatField(
        verbose_name=f'manganeso',
        blank=True, null=True,
        help_text=f'Manganeso'
    )  		
    od = models.FloatField(
        verbose_name=f'o.d.',
        blank=True, null=True,
        help_text=f'O.D. (%)'
    )  		
    langelie = models.FloatField(
        verbose_name=f'indice de Langelie',
        blank=True, null=True,
        help_text=f'Indice de Langelie (ISL).'
    )  		
    observations =  models.CharField(
        max_length=512,
        verbose_name=f'observaciones',
        blank=True, null=True,
        help_text=f'Observaciones. No debe contener más de 512 caracteres.'
    ) 
    lat = models.FloatField(
        verbose_name=f'latitud',
        blank=True, null=True,
        help_text=f'Latitud del SARH.'
    )
    lon = models.FloatField(
        verbose_name=f'longitud',
        blank=True, null=True,
        help_text=f'Longitud del SARH.'
    )
    geom = PointField(blank=True,null=True)

    class Meta:
        verbose_name = 'Sistema de Autoabastecimiento de Recursos Hídricos (SARH)'
        verbose_name_plural = 'Sistemas de Autoabastecimiento de Recursos Hídricos (SARH)'
        ordering = ['epsa','user',]

    def __str__(self):
        return f'{self.epsa} - {self.user}'
    def get_state(self):
        rel_epsa = EPSA.objects.filter(code=self.epsa)
        if rel_epsa:
            state_code = str(rel_epsa[0].state)
            if state_code in state_code_to_name.keys():
                return state_code_to_name[state_code]
        return ''
    get_state.short_description = 'Departamento'
    def get_sub_subt(self):
        return self.sub_subt
    get_sub_subt.short_description = 'SUB/SUP'




class TecnicalDataSub(models.Model):
    MEDIDOR_CHOICES = (
        ('SI','SI'),
        ('NO','NO'),
    )
    sarh = models.ForeignKey(
        to=SARH,
        on_delete=models.CASCADE,
        related_name='tecnical_sub',
        verbose_name='Datos Técnicos Subterráneo',
        help_text='Datos técnicos subterráneo.',
    )
    detalle = models.CharField(
        max_length = 256,
        verbose_name = 'detalle',
        help_text = 'Detalle del medidor. No puede contener más de 256 caracteres.',
        blank=True, null=True,
    )
    year =	models.IntegerField(
        verbose_name='gestión',
        default=datetime.now().year,
        help_text='Gestión de los datos técnicos. Debe ser un número entero mayor o igual a 1800. Campo obligatorio.',
        validators=[MinValueValidator(1800)],
    )
    tiene_medidor = models.CharField(
        max_length=2,
        choices=MEDIDOR_CHOICES,
        verbose_name='tiene medidor',
        help_text='El pozo tiene medidor (SI o NO).',
        blank=True,null=True,
    )
    vol_extraido_promedio =  models.FloatField(
        verbose_name='volumen extraido promedio',
        blank=True, null=True,
        help_text=f'Volúmen Extraido Promedio (m3/mes)',
    )
    aforo = models.FloatField(
        verbose_name='caudal del SARH',
        blank=True, null=True,
        help_text= 'Caudal del SARH (aforo)(l/s)',
    )
    nivel_estatico = models.FloatField(
        verbose_name='nivel estático',
        blank=True, null=True,
        help_text='Nivel estático (m)',
    )
    nivel_dinamico = models.FloatField(
        verbose_name='nivel dinámico',
        blank=True, null=True,
        help_text=f'Nivel dinámico(m)',
    )
    caudal_optimo = models.FloatField(
        verbose_name='caudal óptimo',
        blank=True, null=True,
        help_text=f'Caudal óptimo(l/s)',
    )
    class Meta:
        verbose_name = 'Datos Técnicos Superficiales'
        verbose_name_plural = 'Datos Técnicos Superficiales'
        ordering = ['sarh','year',]
    def __str__(self):
        return f'{self.sarh} - {self.year}'


class TecnicalDataSup(models.Model):
    MEDIDOR_CHOICES = (
        ('SI','SI'),
        ('NO','NO'),
    )
    sarh = models.ForeignKey(
        to=SARH,
        on_delete=models.CASCADE,
        related_name='tecnical_sup',
        verbose_name='datos técnicos superficial',
        help_text='Datos técnicos superficial.',
    )
    detalle = models.CharField(
        max_length = 256,
        verbose_name = 'detalle',
        help_text = 'Detalle del medidor. No puede contener más de 256 caracteres.',
        blank=True, null=True,
    )
    year =	models.IntegerField(
        verbose_name='gestión',
        default=datetime.now().year,
        help_text='Gestión de los datos técnicos. Debe ser un número entero mayor o igual a 1800. Campo obligatorio.',
        validators=[MinValueValidator(1800)],
    )
    tiene_medidor = models.CharField(
        max_length=2,
        choices=MEDIDOR_CHOICES,
        verbose_name='tiene medidor',
        help_text='El pozo tiene medidor (SI o NO).',
        blank=True,null=True,
    )
    vol_extraido_promedio =  models.FloatField(
        verbose_name='volumen extraido promedio',
        blank=True, null=True,
        help_text=f'Volúmen Extraido Promedio (m3/mes)',
    )  		
    caudal_lluvia = models.FloatField(
        verbose_name='caudal época de lluvial',
        blank=True, null=True,
        help_text= 'Caudal época de lluvial Qll (m3/s)',
    )  		
    caudal_estiaje = models.FloatField(
        verbose_name='caudal época de estiaje',
        blank=True, null=True,
        help_text='Caudal época de estiaje Qe (m3/s)',
    )
    caudal_medio_anual = models.FloatField(
        verbose_name='caudal medio anual',
        blank=True, null=True,
        help_text=f'Caudal medio anual Qma (m3/s)',
    )
    caudal_eco = models.FloatField(
        verbose_name='caudal ecológico',
        blank=True, null=True,
        help_text=f'Caudal ecológico (m3/s)',
    )
    class Meta:
        verbose_name = 'Datos Técnicos Superficiales'
        verbose_name_plural = 'Datos Técnicos Superficiales'
        ordering = ['sarh','year',]
    def __str__(self):
        return f'{self.sarh} - {self.year}'
