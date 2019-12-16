import json
from django.core import serializers
from supply_areas.models import SupplyArea
from rest_framework import viewsets, response, serializers

class SupplyAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyArea
        fields = '__all__'

class SupplyAreaViewSet(viewsets.ModelViewSet):
    
    queryset = SupplyArea.objects.all()
    serializer_class = SupplyAreaSerializer
    '''
    list:
    Retorna un conjunto de instancias del modelo `SupplyAreas` (áreas de prestación de servicios).

    La respuesta obtenida es en formato GeoJSON donde los "features" son los polígonos de las áreas de cobertura.
    
    Soporta los siguientes parámetros de filtro: `epsa` y `state` que representan la sigla de la EPSA y el departamento del área de cobertura respectivamente.

        /api/supply_areas/?state=SC
    
    retorna todas las áreas de prestación de servicios de EPSAs de Santa Cruz. Si ningún parámetro es dado, retorna todas las instancias disponibles.

    Los campos disponibles para cada instancia son: `epsa` y `area` que representan la sigla de la EPSA y el área del polígono respectivamente. Estos datos son retornados bajo la llave "properties" de cada "feature". Además, el polígono de cada área es retornado bajo la llave "geometry". 

    Por ejemplo, el pedido

        GET /api/supply_areas/?epsa=AAPOS
    
    Retorna el siguiente GeoJSON:

        {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "epsa": "AAPOS",
                        "area": 3243.01
                    },
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [
                                [
                                    [
                                        -65.737329,
                                        -19.606613
                                    ],
                                    ...
                                    [
                                        -65.737329,
                                        -19.606613
                                    ]
                                ]
                            ]
                        ]
                    }
                }
            ],
            "crs": {
                "type": "link",
                "properties": {
                    "href": "http://spatialreference.org/ref/epsg/4326/",
                    "type": "proj4"
                }
            }
        }

    create:
    Este punto de acceso permite el ingreso de instancias del modelo `SupplyAreas` (áreas de prestación de servicios) al sistema.

    El pedido HTTP debe ser del tipo `POST` y el cuerpo del pedido debe ser un objeto codificado del tipo GeoJSON con las propiedades `epsa`, `area`, que representan la sigla de la EPSA del área de prestación de servicios ingresada.

    Las instancias pueden ser añadidas al sistema una a la vez o pueden ser ingresadas en masa agregando "features" al GeoJSON. Por ejemplo,   

        {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "epsa": "AAPOS",
                        "area": 3243.01
                    },
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [
                                [
                                    [
                                        -65.737329,
                                        -19.606613
                                    ],
                                    ...
                                    [
                                        -65.737329,
                                        -19.606613
                                    ]
                                ]
                            ]
                        ]
                    }
                }, {
                    "type": "Feature",
                    "properties": {
                        "epsa": "COOAPASH",
                        "area": 230.02
                    },
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [
                                [
                                    [
                                        -65.241591,
                                        -16.99835
                                    ],
                                    ...
                                    [
                                        -65.241591,
                                        -16.99835
                                    ]
                                ]
                            ]
                        ]
                    }
                }
            ],
            "crs": {
                "type": "link",
                "properties": {
                    "href": "http://spatialreference.org/ref/epsg/4326/",
                    "type": "proj4"
                }
            }
        }

    Añadiría las áreas de prestación de servicios de las EPSAs AAPOS y COOAPASH al sistema. 

    Si los objetos ingresados no pasan el proceso de validación del sistema, las instancias no serán creadas y el error será retornado como respuesta al pedido.
    '''
    def list(self, request):
        queryset = SupplyArea.objects.all()

        state = request.query_params.get('state', None)
        epsa_code = request.query_params.get('epsa', None)
        if state is not None:
            queryset = queryset.filter(epsa__state=state)
        if epsa_code is not None:
            queryset = queryset.filter(epsa__code=epsa_code)
            
        options = dict(
            properties=['epsa',],
            geometry_field='geom',
            precision=None,
            simplify=None,
            force2d=False,
            bbox=None,
            bbox_auto=False,
            use_natural_keys=False,
            with_modelname=False,
            ensure_ascii=False
        )
        data = json.loads(serializers.serialize('geojson', queryset, **options))
        for feat in data['features']:
            del feat['id']
            if 'model' in feat['properties']:
                del feat['properties']['model']

        return response.Response(data)

    def create(self, request):
        try:
            json_str = request.body.decode('utf-8')
            for serobj in serializers.deserialize('geojson', json_str, model_name='supply_areas.SupplyArea'):
                serobj.save()
            return response.Response(dict(created_obj=json_str))
        except Exception as e:
            return response.Response(dict(error=str(e)))

