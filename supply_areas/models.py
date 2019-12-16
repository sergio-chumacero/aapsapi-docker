from django.db import models
from djgeojson.fields import MultiPolygonField
from performance.models import EPSA, BaseModel

class SupplyArea(models.Model):
    epsa = models.CharField(
        max_length = 32,
        verbose_name = 'sigla EPSA',
        help_text = 'Sigla de la EPSA. No debe contenter más de 32 caracteres.'
    )
    geom = MultiPolygonField(blank=True, null=True)

    class Meta:
        verbose_name = 'Área de Prestación de Servicio'
        verbose_name_plural = 'Áreas de Prestación de Servicio'
        ordering = ['epsa',]

    def __str__(self):
        return f'({self.id}) {self.epsa}'