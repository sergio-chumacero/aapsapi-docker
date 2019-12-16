from rest_framework import viewsets
from ambiental import models, serializers
from rest_framework.response import Response
from rest_framework import status

class CustomViewSet(viewsets.ModelViewSet):
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CustomViewSet, self).get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.initial_data)
        return Response(serializer.instance, status=status.HTTP_201_CREATED)

class SARHViewSet(CustomViewSet):
    serializer_class = serializers.SARHSerializer
    queryset = models.SARH.objects.all()
    filterset_fields = ('epsa',)

# import json
# from django.core import serializers
# from ambiental.models import SARH
# from rest_framework import viewsets, response

# class SARHViewSet(viewsets.ViewSet):
#     '''
#     list:
#     Retorna un conjunto de instancias del modelo `SARH` (Sistemas de Autoabastecimiento de Recursos Hídricos).

#     La respuesta obtenida es en formato GeoJSON donde los "features" son los puntos georeferenciados de los SARH.
    
#     Soporta los siguientes parámetros de filtro: `epsa` y `state` que representan la sigla de la EPSA y el departamento del SARH. Por ejemplo,

#         /api/sarh/?state=SC
    
#     retorna todos los SARH de EPSAs de Santa Cruz. Si ningún parámetro es dado, retorna todas las instancias disponibles.

#     Los campos disponibles para cada instancia son: `epsa` y `area` que representan la sigla de la EPSA y el área del polígono respectivamente. Estos datos son retornados bajo la llave "properties" de cada "feature". Además, el polígono de cada área es retornado bajo la llave "geometry". 

#     Por ejemplo, el pedido

#         GET /api/supply_areas/?epsa=AAPOS
    
#     Retorna el siguiente GeoJSON:

#         {
#             "type": "FeatureCollection",
#             "features": [
#                 {
#                     "type": "Feature",
#                     "properties": {
#                         "epsa": "AAPOS",
#                         "area": 3243.01
#                     },
#                     "geometry": {
#                         "type": "MultiPolygon",
#                         "coordinates": [
#                             [
#                                 [
#                                     [
#                                         -65.737329,
#                                         -19.606613
#                                     ],
#                                     ...
#                                     [
#                                         -65.737329,
#                                         -19.606613
#                                     ]
#                                 ]
#                             ]
#                         ]
#                     }
#                 }
#             ],
#             "crs": {
#                 "type": "link",
#                 "properties": {
#                     "href": "http://spatialreference.org/ref/epsg/4326/",
#                     "type": "proj4"
#                 }
#             }
#         }

#     create:
#     Este punto de acceso permite el ingreso de instancias del modelo `SupplyAreas` (áreas de prestación de servicios) al sistema.

#     El pedido HTTP debe ser del tipo `POST` y el cuerpo del pedido debe ser un objeto codificado del tipo GeoJSON con las propiedades `epsa`, `area`, que representan la sigla de la EPSA del área de prestación de servicios ingresada.

#     Las instancias pueden ser añadidas al sistema una a la vez o pueden ser ingresadas en masa agregando "features" al GeoJSON. Por ejemplo,   

#         {
#             "type": "FeatureCollection",
#             "features": [
#                 {
#                     "type": "Feature",
#                     "properties": {
#                         "epsa": "AAPOS",
#                         "area": 3243.01
#                     },
#                     "geometry": {
#                         "type": "MultiPolygon",
#                         "coordinates": [
#                             [
#                                 [
#                                     [
#                                         -65.737329,
#                                         -19.606613
#                                     ],
#                                     ...
#                                     [
#                                         -65.737329,
#                                         -19.606613
#                                     ]
#                                 ]
#                             ]
#                         ]
#                     }
#                 }, {
#                     "type": "Feature",
#                     "properties": {
#                         "epsa": "COOAPASH",
#                         "area": 230.02
#                     },
#                     "geometry": {
#                         "type": "MultiPolygon",
#                         "coordinates": [
#                             [
#                                 [
#                                     [
#                                         -65.241591,
#                                         -16.99835
#                                     ],
#                                     ...
#                                     [
#                                         -65.241591,
#                                         -16.99835
#                                     ]
#                                 ]
#                             ]
#                         ]
#                     }
#                 }
#             ],
#             "crs": {
#                 "type": "link",
#                 "properties": {
#                     "href": "http://spatialreference.org/ref/epsg/4326/",
#                     "type": "proj4"
#                 }
#             }
#         }

#     Añadiría las áreas de prestación de servicios de las EPSAs AAPOS y COOAPASH al sistema. 

#     Si los objetos ingresados no pasan el proceso de validación del sistema, las instancias no serán creadas y el error será retornado como respuesta al pedido.
#     '''
#     def list(self, request):
#         queryset = SARH.objects.all()

#         state = request.query_params.get('state', None)
#         epsa_code = request.query_params.get('epsa', None)
#         if state is not None:
#             queryset = queryset.filter(epsa__state=state)
#         if epsa_code is not None:
#             queryset = queryset.filter(epsa__code=epsa_code)
            
#         options = dict(
#             properties=[
#                 'epsa','user','folder_code','sarh_denom',
#                 'rar_aaps_nr','rar_date','aaps_notification_date','user_notification_date','auth_year',
#                 'condition','reg_renov','renovation_alert',
#                 'auth_certificate_state','state', 'active_inactive_sealed','source_nr','discharge_place',
#                 'municipality','industry_type','user_description','form_extraction_volume','authorized_streamflow',
#                 'anual_volume','observations',
#                 'ph','conductivity','turbidity','iron','manganese','od','water_quality','other',
#                 'x','y','z','zone','lat','lon'
#             ],
#             geometry_field='geom',
#             precision=None,
#             simplify=None,
#             force2d=False,
#             bbox=None,
#             bbox_auto=False,
#             use_natural_keys=False,
#             with_modelname=False,
#             ensure_ascii=False
#         )
#         data = json.loads(serializers.serialize('geojson', queryset, **options))
#         for feat in data['features']:
#             del feat['id']
#             if 'model' in feat['properties']:
#                 del feat['properties']['model']

#         return response.Response(data)

#     def create(self, request):
#         try:
#             json_str = request.body.decode('utf-8')
#             for serobj in serializers.deserialize('geojson', json_str, model_name='ambiental.SARH'):
#                 serobj.save()
#             return response.Response(dict(created_obj=json_str))
#         except Exception as e:
#             return response.Response(dict(error=str(e)))

