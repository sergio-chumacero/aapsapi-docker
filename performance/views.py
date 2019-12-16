from rest_framework import viewsets
from performance import models, serializers
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

class EPSAViewSet(CustomViewSet):
    '''
    list:
    Retorna un conjunto de instancias del modelo `EPSA`.
    
    Soporta los siguientes parámetros de filtro: `code`, `state` y `category`. Por ejemplo,

        /api/epsas/?state=SC&category=C
    
    retorna todas las EPSA de categoría C de Santa Cruz. Si ningún parámetro es dado, retorna todas las instancias disponibles.

    Los campos disponibles para cada instancia son: `code`, `name`, `state` y `category`.

    Al igual que las instancias, los campos de cada instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        /api/epsas/?fields=code,category
    
    retorna sólamente la sigla y la categoría de todas las EPSA en el sistema.

    create:
    Este punto de acceso permite la creación instancias del modelo `EPSA` en el sistema.

    El pedido HTTP debe ser del tipo `POST` y el cuerpo del pedido debe ser un objeto codificado del tipo `json` con los campos `code`, `name`, `state` y `category`, que representan la sigla, nombre, departamento y categoría de la EPSA ingresada.

    Las instancias pueden ser añadidas al sistema una a la vez o pueden ser ingresadas en masa agrupando a los objetos a ingresar en una lista en el JSON del pedido. Por ejemplo,

        [
            {
                "code": "EPSAS",
                "name": "Empresa Pública Social De Agua y Saneamiento",
                "state": "LP",
                "category": "A"
            }, {
                "code": "SAGUAPAC",
                "name": "Cooperativa de Servicios Públicos Santa Cruz S.R.L.",
                "state": "SC",
                "category": "A"
            }
        ]

    Añadiría las instancias correspondientes a EPSAS y SAGUAPAC al sistema. 

    Si los objetos ingresados no pasan el proceso de validación del sistema, las instancias no serán creadas y el error será retornado como respuesta al pedido.

    Si la sigla de una de las EPSA en creación coincide con la de una instancia que ya se encuentre en el sistema los atributos de esta serán actualizados. 

    read:
    Retorna una instancia específica del modelo `EPSA`.

    El modelo `EPSA` tiene como llave primaria el campo `code` (sigla) y este campo debe ser utilizado para identificar la EPSA a retornar. Por ejemplo,

        /api/epsas/AAPOS/
    
    retorna la instancia de `EPSA` correspondiente a la EPSA AAPOS.

    Los campos disponibles para cada instancia son: `code`, `name`, `state` y `category`.

    Los campos de la instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        /api/epsas/AAPOS/?fields=code,category
    
    retorna sólamente la sigla y la categoría de la instancia de `EPSA` correspondiente a la EPSA AAPOS.
    
    update:
    Este punto de acceso permite la edición de una instancia del modelo `EPSA` que se encuentre actualmente en el sistema.

    El modelo `EPSA` tiene como llave primaria el campo `code` (sigla) y este campo debe ser utilizado para identificar la EPSA a editar. Por ejemplo,

        PUT /api/epsas/AAPOS/

    modificaría la instancia de `EPSA` correspondiente a la EPSA AAPOS.

    El pedido HTTP debe ser del tipo `PUT` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos nuevos `code`, `name`, `state` y `category`, que representan la sigla, nombre, departamento y categoría de la EPSA editada. Por ejemplo,

    Por ejemplo,

        {
            "code": "<nueva sigla>",
            "name": "<nuevo nombre>,
            "state": "<nuevo departamento>",
            "category": "<nueva categoría>"
        }
    
    Reemplazaría los campos de la EPSA AAPOS por los nuevos valores. 

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será modificada y el error será retornado como respuesta al pedido.

    partial_update:
    Este punto de acceso permite la edición parcial de una instancia del modelo `EPSA` que se encuentre actualmente en el sistema.

    El modelo `EPSA` tiene como llave primaria el campo `code` (sigla) y este campo debe ser utilizado para identificar la EPSA a editar. Por ejemplo,

        PATCH /api/epsas/AAPOS/

    modificaría la instancia de `EPSA` correspondiente a la EPSA AAPOS.

    El pedido HTTP debe ser del tipo `PATCH` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con algunos de los campos `code`, `name`, `state` y `category`, que representan la sigla, nombre, departamento y categoría de la EPSA editada. Por ejemplo,

    Sólamente los campos incluidos serán modificados, mientras aquellos no incluidos serán mantenidos con su valor actual.
    Por ejemplo,

        {
            "name": "<nuevo nombre>
        }
    
    Cambiaría sólamente el nombre de la EPSA AAPOS en el sistema.

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será modificada y el error será retornado como respuesta al pedido.

    delete:
    Elimina una instancia específica del modelo `EPSA`.

    El modelo `EPSA` tiene como llave primaria el campo `code` (sigla) y este campo debe ser utilizado para identificar la EPSA a eliminar. Por ejemplo,

        DELETE /api/epsas/AAPOS/
    
    elimina la instancia de `EPSA` correspondiente a la EPSA AAPOS.
    '''
    serializer_class = serializers.EPSASerializer
    queryset = models.EPSA.objects.all()
    filterset_fields = ('code','state','category',)


class VariableViewSet(CustomViewSet):
    '''
    list:
    Retorna un conjunto de instancias del modelo `Variable`.
    
    Soporta los siguientes parámetros de filtro: `code` y `var_id`. Es decir el código e índice de la variable respectivamente. Por ejemplo,

        /api/variables/?code=vol_ap
        /api/variables/?var_id=3
    
    cualquiera de las dos retorna la instancia correspondiente a la variable de "Volumen de agua potable producido". Si ningún parámetro es dado, retorna todas las instancias disponibles.

    Los campos disponibles para cada instancia son: `code`, `var_id`, `name`, `unit` y `var_type`, que representan el código, índice, nombre, unidad y tipo de una variable respectivamente.

    Al igual que las instancias, los campos de cada instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        /api/variables/?fields=name,unit
    
    retorna sólamente el nombre y la unidad de todas las variables en el sistema.

    create:
    Este punto de acceso permite el ingreso de instancias del modelo `Variable` al sistema.

    El pedido HTTP debe ser del tipo `POST` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `code`, `var_id`, `name`, `unit` y `var_type`, que representan el código, índice, nombre, unidad y tipo de la variable ingresada respectivamente.

    Las instancias pueden ser añadidas al sistema una a la vez o pueden ser ingresadas en masa agrupando a los objetos a ingresar en una lista en el JSON del pedido. Por ejemplo,

        [
            {
                "var_id": 1,
                "name": "Volumen de agua cruda extraído de la(s) fuente(s) superficial(es)",
                "unit": "m3/periodo", 
                "var_type": "volumen",
                "code": "vol_sup"
            }, {
                "var_id": 2,
                "name": "Volumen de agua cruda extraído de la(s) fuente(s) subterránea(s)",
                "unit": "m3/periodo",
                "var_type": "volumen",
                "code": "vol_sub"
            }
        ]

    Añadiría las instancias correspondientes a las variables de "Volumen de agua superficial" y "Volumen de agua subterránea" al sistema. 

    Si los objetos ingresados no pasan el proceso de validación del sistema, las instancias no serán creadas y el error será retornado como respuesta al pedido.

    read:
    Retorna una instancia específica del modelo `Variable`.

    El modelo `Variable` tiene como llave primaria el campo `code` (código de variable) y este campo debe ser utilizado para identificar la variable a retornar. Por ejemplo,

        /api/variables/vol_sup/
    
    retorna la instancia de `Variable` correspondiente a la variable de volumen extraído de fuentes superficiales.

    Los campos disponibles para cada instancia son: `code`, `var_id`, `name`, `unit` y `var_type`, que representan el código, índice, nombre, unidad y tipo de una variable respectivamente.

    Los campos de la instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        /api/variables/vol_sup/?fields=var_id,name
    
    retorna sólamente el índice y el nombre de la instancia de `Variable` correspondiente a la variable de volumen extraído de fuentes superficiales.
    
    update:
    Este punto de acceso permite la edición de instancias del modelo `Variable` que se encuentran actualmente en el sistema.

    El modelo `Variable` tiene como llave primaria el campo `code` (código de variable) y este campo debe ser utilizado para identificar la variable a editar. Por ejemplo,

        /api/epsas/vol_sup/

    modificaría la instancia de `Variable` correspondiente a volumen superficial.

    El pedido HTTP debe ser del tipo `PUT` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `code`, `var_id`, `name`, `unit` y `var_type`, que representan el código, índice, nombre, unidad y tipo de la variable editada respectivamente.

    Por ejemplo,

        {
            "var_id": <nuevo índice de la variable>,
            "name": "<nuevo nombre de la variable>",
            "unit": "<nueva unidad de la variable>",
            "var_type": "<nuevo tipo de la variable>",
            "code": "<nuevo código de la variable>"
        }
    
    Reemplazaría los campos de la variable de volumen superficial por los nuevos valores. 

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será editada y el error será retornado como respuesta al pedido.

    partial_update:
    Este punto de acceso permite la edición parcial de una instancia del modelo `Variable` que se encuentre actualmente en el sistema.

    El modelo `Variable` tiene como llave primaria el campo `code` (código de variable) y este campo debe ser utilizado para identificar la Variable a editar. Por ejemplo,

        PATCH /api/variables/vol_sup/

    modificaría la instancia de `Variables` correspondiente a la variable de volumen superficial.

    El pedido HTTP debe ser del tipo `PATCH` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `code`, `var_id`, `name`, `unit` y `var_type`, que representan el código, índice, nombre, unidad y tipo de la variable editada respectivamente.

    Sólamente los campos incluidos serán modificados, mientras aquellos no incluidos serán mantenidos con su valor actual.
    Por ejemplo,

        {
            "name": "<nuevo nombre>
        }
    
    Cambiaría sólamente el nombre de la variable de volumen superficial en el sistema.

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será modificada y el error será retornado como respuesta al pedido.

    delete:
    Elimina una instancia específica del modelo `Variable`.

    El modelo `Variable` tiene como llave primaria el campo `code` (código de la variable) y este campo debe ser utilizado para identificar la variable a eliminar. Por ejemplo,

        DELETE /api/variables/vol_sup/
    
    elimina la instancia de `Variable` correspondiente a la variable de volumen superficial.
    '''
    serializer_class = serializers.VariableSerializer
    queryset = models.Variable.objects.all()
    filterset_fields = ('code','var_id')

class IndicatorViewSet(CustomViewSet):
    '''
    list:
    Retorna un conjunto de instancias del modelo `Indicator` (indicador).
    
    Soporta los siguientes parámetros de filtro: `code` y `ind_id`. Es decir el código e índice del indicador respectivamente. Por ejemplo,

        /api/indicators/?code=cobertura_ap
        /api/indicators/?ind_id=8
    
    cualquiera de las dos retorna la instancia correspondiente al indicador de "Cobertura del servicio de agua potable". Si ningún parámetro es dado, retorna todas las instancias disponibles.

    Los campos disponibles para cada instancia son: `code`, `ind_id`, `name`, `unit`, `criteria`, `par_min_A`...`par_min_D` y `par_max_A`...`par_max_D`, que representan el código, índice, nombre, unidad, criterio y parámetros óptimos del indicador ingresado respectivamente.
    Al igual que las instancias, los campos de cada instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        /api/variables/?fields=name,unit
    
    retorna sólamente el nombre y la unidad de todas los indicadores en el sistema.

    create:
    Este punto de acceso permite el ingreso de instancias del modelo `Indicator` (indicador) al sistema.

    El pedido HTTP debe ser del tipo `POST` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `code`, `ind_id`, `name`, `unit`, `criteria`, `par_min_A`...`par_min_D` y `par_max_A`...`par_max_D`, que representan el código, índice, nombre, unidad, criterio y parámetros óptimos del indicador ingresado respectivamente.

    Las instancias pueden ser añadidas al sistema una a la vez o pueden ser ingresadas en masa agrupando a los objetos a ingresar en una lista en el JSON del pedido. Por ejemplo,

        [
            {
                "code": "continuidad_corte",
                "name": "Continuidad por corte",
                "criteria": "abastecimiento",
                "unit": "%", 
                "par_min_A": 95.0, "par_min_B": 90.0, "par_min_C": 95.0, "par_min_D": 95.0, 
                "par_max_A": null, "par_max_B": null, "par_max_C": null, "par_max_D": null, 
                "ind_id": 7
            }, {
                "code": "continuidad_racionamiento",
                "name": "Continuidad por racionamiento",
                "criteria": "abastecimiento", 
                "unit": "hr/día",
                "par_min_A": 20.0, "par_min_B": 20.0, "par_min_C": 12.0, "par_min_D": 8.0,
                "par_max_A": null, "par_max_B": null, "par_max_C": null, "par_max_D": null,
                "ind_id": 6
            }
        ]

    Añadiría las instancias correspondientes a los indicadores "Continuidad por corte" y "Continuidad por racionamiento" al sistema. 

    Si los objetos ingresados no pasan el proceso de validación del sistema, las instancias no serán creadas y el error será retornado como respuesta al pedido.

    read:
    Retorna una instancia específica del modelo `Indicator` (indicador).

    El modelo `Indicator` tiene como llave primaria el campo `code` (código de indicador) y este campo debe ser utilizado para identificar el indicador a retornar. Por ejemplo,

        /api/indicators/rendimiento_actual_fuente/
    
    retorna la instancia de `Indicator` correspondiente al indicador de rendimiento actual de la fuente.

    Los campos disponibles para cada instancia son: `code`, `ind_id`, `name`, `unit`, `criteria`, `par_min_A`...`par_min_D` y `par_max_A`...`par_max_D`, que representan el código, índice, nombre, unidad, criterio y parámetros óptimos del indicador ingresado respectivamente.

    Los campos de la instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        /api/indicators/rendimiento_acutal_fuente/?fields=ind_id,name
    
    retorna sólamente el índice y el nombre de la instancia de `Indicator` correspondiente al indicador de rendimiento actual de la fuente.

    update:
    Este punto de acceso permite la edición de una instancia del modelo `Indicator` (indicador) que se encuentran actualmente en el sistema.

    El modelo `Indicator` tiene como llave primaria el campo `code` (código del indicador) y este campo debe ser utilizado para identificar la variable a editar. Por ejemplo,

        /api/indicators/cobertura_ap/

    modificaría la instancia de `Indicator` correspondiente a la cobertura de agua potable.

    El pedido HTTP debe ser del tipo `PUT` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `code`, `ind_id`, `name`, `unit`, `criteria`, `par_min_A`...`par_min_D` y `par_max_A`...`par_max_D`, que representan el código, índice, nombre, unidad, criterio y parámetros óptimos del indicador ingresado respectivamente.

    Por ejemplo,

        {
            "code": "<nuevo código de la variable>",
            "name": "<nuevo nombre de la variable>",
            "criteria": "<nuevo criterio de la variable>", 
            "unit": "<nueva unidad de la variable>",
            "par_min_A": <nuevo valor del parámetro mínimo para categoría A>, ... ,  "par_min_D": <...>,
            "par_max_A": <nuevo valor del parámetro máximo para categoría A>, ... , "par_max_D": <...>,
            "ind_id": <nuevo índice del indicador>
        }
    
    Reemplazaría los campos del indicador de cobertura de agua potable por los nuevos valores. 

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será editada y el error será retornado como respuesta al pedido.

    partial_update:
    Este punto de acceso permite la edición parcial de una instancia del modelo `Indicator` (indicador) que se encuentre actualmente en el sistema.

    El modelo `Indicator` tiene como llave primaria el campo `code` (código del indicador) y este campo debe ser utilizado para identificar el indicador a editar. Por ejemplo,

        PATCH /api/indicators/cobertura_ap/

    modificaría la instancia de `Indicator` correspondiente al indicador de cobertura de agua potable.

    El pedido HTTP debe ser del tipo `PUT` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `code`, `ind_id`, `name`, `unit`, `criteria`, `par_min_A`...`par_min_D` y `par_max_A`...`par_max_D`, que representan el código, índice, nombre, unidad, criterio y parámetros óptimos del indicador ingresado respectivamente.

    Sólamente los campos incluidos serán modificados, mientras aquellos no incluidos serán mantenidos con su valor actual.
    Por ejemplo,

        {
            "name": "<nuevo nombre>
        }
    
    Cambiaría sólamente el nombre del indicador de cobertura de agua potable en el sistema.

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será modificada y el error será retornado como respuesta al pedido.

    delete:
    Elimina una instancia específica del modelo `Indicator` (indicador).

    El modelo `Indicator` tiene como llave primaria el campo `code` (código del indiador) y este campo debe ser utilizado para identificar el indicador a eliminar. Por ejemplo,

        DELETE /api/indicators/cobertura_ap/
    
    elimina la instancia de `Indicator` correspondiente al indicador de cobertura de agua potable.
    '''
    serializer_class = serializers.IndicatorSerializer
    queryset = models.Indicator.objects.all()
    filterset_fields = ('code','ind_id')

class VariableReportViewSet(CustomViewSet):
    '''
    list:
    Retorna un conjunto de instancias del modelo `VariableReport` (reporte de variables).
    Este modelo representa un reporte completo de variables de una epsas en un año o mes.
    
    Este punto de acceso soporta los siguientes parámetros de filtro: `epsa`, `year` y `month`. Es decir la EPSA, el año y el mes del reporte respectivamente. Por ejemplo,

        /api/reports/?epsa=AAPOS&year=2017
    
    retorna la instancia correspondiente al reporte de variables de la epsa AAPOS del año 2017. Si ningún parámetro es dado, retorna todas las instancias disponibles.

    Los campos disponibles para cada instancia son: `epsa`, `year`, `month`, `v1`...`v51` y `v1_type`...`v51_type`, que representan la epsa, año, mes, valores y tipos de los valores de un reporte respectivamente.

    Al igual que las instancias, los campos de cada instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        /api/variables/?fields=epsa,v1&year=2017
    
    retorna sólamente el nombre de la epsa y el valor de la variable 1 y de los reportes del año 2017.

    create:
    Este punto de acceso permite el ingreso de instancias del modelo `VariableReport` (reporte de variables) al sistema.

    El pedido HTTP debe ser del tipo `POST` y cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `epsa`, `year`, `month`, `v1`...`v51` y `v1_type`...`v51_type`, que representan la epsa, año, mes, valores y tipos de los valores de un reporte respectivamente.

    Las instancias pueden ser añadidas al sistema una a la vez o pueden ser ingresadas en masa agrupando a los objetos a ingresar en una lista en el JSON del pedido. Por ejemplo,


        [
            {
                "year": 2017, 
                "v1": "790840.00", "v1_type": "VA",
                "v2": "531163.00", "v2_type": "VA",
                ...
                "v51": null, "v51_type": "VA", 
                "epsa": "6 DE OCTUBRE", 
                "month": null
            }, {
                "year": 2014, 
                "v1": "10738512.20", "v1_type": "VA", 
                "v2": null, "v2_type": "VA", 
                ...
                "v51": "248.69", "v51_type": "VA",
                "epsa": "AAPOS",
                "month": null
            }
        ]

    Añadiría las instancias correspondientes a los reportes de variables de las EPSAs 6 DE OCTUBRE y AAPOS de los años 2017 y 2014 respectivamente.

    Si los objetos ingresados no pasan el proceso de validación del sistema, las instancias no serán creadas y el error será retornado como respuesta al pedido.

    read:
    Retorna una instancia específica del modelo `VariableReport` (reporte de variables).

    El modelo `VariableReport` tiene como llave primaria el campo `id` (índice del reporte de variables) y este campo debe ser utilizado para identificar el indicador a retornar. Por ejemplo,

        /api/reports/1/
    
    retorna la instancia de `VariableReport` correspondiente al reporte con índice 1.

    Los campos disponibles para cada instancia son: `epsa`, `year`, `month`, `v1`...`v51` y `v1_type`...`v51_type`, que representan la epsa, año, mes, valores y tipos de los valores de un reporte respectivamente.

    Los campos de la instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        /api/reports/1/?fields=epsa,year,v1
    
    retorna sólamente la sigla de la EPSA, el año y el valor de la variable de la instancia de `VariableReport` con el índice 1.

    **Nota:** El campo `id` es usado en el modelo interno del sistema.
    Para identificar de manera única una instancia `VariableReport` sin hacer uso de este campo, es posible usar la combinación de los campos `epsa`, `year` y `month`,
    que es garantizada de ser única entre reportes a través del proceso de validación del sistema. De esta manera el punto de acceso `list` también implementa el punto de acceso `read`. Por ejemplo,

        GET /api/reports/?epsa=AAPOS&year=2017&month=6

    retorna la instancia única de reporte de variables de la EPSA AAPOS de Junio de 2017.

    update:
    Este punto de acceso permite la edición de una instancia del modelo `VariableReport` (reporte de variables) que se encuentre actualmente en el sistema.

    El modelo `VariableReport` tiene como llave primaria el campo `id` (índice del reporte de variables) y este campo debe ser utilizado para identificar la instancia a editar. Por ejemplo,

        PUT /api/reports/1/

    modificaría la instancia de `VariableReport` con índice 1.

    El pedido HTTP debe ser del tipo `PUT` y cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `epsa`, `year`, `month`, `v1`...`v51` y `v1_type`...`v51_type`, que representan la epsa, año, mes, valores y tipos de los valores de un reporte respectivamente.

    Por ejemplo,

        {
            "year": <nuevo año>, 
            "v1": <nuevo valor variable 1>, "v1_type": "<nuevo tipo de la variable 1>",
            "v2": <nuevo valor variable 2>, "v2_type": "<nuevo tipo de la variable 2>",
            ...
            "v51": <nuevo valor variable 51>, "v51_type": "<nuevo tipo de la variable 51>", 
            "epsa": "<sigla de la nueva EPSA>", 
            "month": <nuevo mes>
        }
    
    Reemplazaría los campos del reporte de variables con índice 1 por los nuevos valores. 

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será editada y el error será retornado como respuesta al pedido.

    partial_update:
    Este punto de acceso permite la edición parcial de una instancia del modelo `VariableReport` (reporte de variables) que se encuentre actualmente en el sistema.

    El modelo `VariableReport` tiene como llave primaria el campo `id` (índice del reporte de variables) y este campo debe ser utilizado para identificar el indicador a editar. Por ejemplo,

        PATCH /api/reports/5/

    modificaría la instancia de `VariableReport` con el índice 5.

    El pedido HTTP debe ser del tipo `PATCH` y cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con algunaos de los  los campos `epsa`, `year`, `month`, `v1`...`v51` y `v1_type`...`v51_type`, que representan la epsa, año, mes, valores y tipos de los valores de un reporte respectivamente.

    Sólamente los campos incluidos serán modificados, mientras aquellos no incluidos serán mantenidos con su valor actual.
    Por ejemplo,

        {
            "v3": <nuevo valor de la variable 3>
        }
    
    Cambiaría sólamente el campo de la variable 3 del reporte de variables con el índice 5.

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será modificada y el error será retornado como respuesta al pedido.

    delete:
    Elimina una instancia específica del modelo `VariableReport` (reporte de variables).

    El modelo `VariableRport` tiene como llave primaria el campo `id` (índice del reporte de variables) y este campo debe ser utilizado para identificar el reporte de variables a eliminar. Por ejemplo,

        DELETE /api/reports/7/
    
    elimina la instancia de `VariableReport` correspondiente al reporte de variables con el índice 7.
    '''
    serializer_class = serializers.VariableReportSerializer
    queryset = models.VariableReport.objects.all()
    filterset_fields = ('epsa','year','month',)

class IndicatorMeasurementViewSet(CustomViewSet):
    '''
    list:
    Retorna un conjunto de instancias del modelo `IndicatorMeasurement` (medidad de indicadores).
    Este modelo representa los indicadores calculadoes en base a un reporte completo de variables completo en un año o mes.
    
    Este punto de acceso soporta los siguientes parámetros de filtro: `epsa`, `year` y `month`. Es decir la EPSA, el año y el mes del reporte sobre el cual se calcularon los indicadores respectivamente. Por ejemplo,

        /api/reports/?epsa=AAPOS&year=2017
    
    retorna la instancia correspondiente a los indicadores de la epsa AAPOS del año 2017. Si ningún parámetro es dado, retorna todas las instancias disponibles.

    Los campos disponibles para cada instancia son: `epsa`, `year`, `month` y `ind1`...`ind32`, que representan la epsa, año, mes y los valores de los indicadores respectivamente.

    Al igual que las instancias, los campos de cada instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        /api/variables/?fields=epsa,ind1&year=2017
    
    retorna sólamente el nombre de la epsa y el valor del indicador 1 y del año 2017.
    
    create:
    Este punto de acceso permite el ingreso de instancias del modelo `IndicatorMeasurement` (medida de indicadores) al sistema.

    El pedido HTTP debe ser del tipo `POST` y cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `epsa`, `year`, `month` y `ind1`...`ind32`, que representan la epsa, año, mes y los valores de los indicadores respectivamente.

    Las instancias pueden ser añadidas al sistema una a la vez o pueden ser ingresadas en masa agrupando a los objetos a ingresar en una lista en el JSON del pedido. Por ejemplo,


        [
            {
                "year": 2017, 
                "ind1": "51.75",
                "ind2": "72.11",
                ... 
                "ind32": "93.81", 
                "epsa": "6 DE OCTUBRE", 
                "month": null
            }, {
                "year": 2014, 
                "ind1": "98.70", 
                "ind2": "85.38",
                "ind32": "67.29",
                "epsa": "AAPOS",
                "month": null
            }
        [

    Añadiría las instancias correspondientes a los indicadores calculadors para las EPSAs 6 DE OCTUBRE y AAPOS de los años 2017 y 2014 respectivamente.

    Si los objetos ingresados no pasan el proceso de validación del sistema, las instancias no serán creadas y el error será retornado como respuesta al pedido.
    read:
    Retorna una instancia específica del modelo `IndicatorMeasurement` (medida de indicadores).

    El modelo `IndicatorMeasurement` tiene como llave primaria el campo `id` (índice de la medida de indicadores) y este campo debe ser utilizado para identificar el indicador a retornar. Por ejemplo,

        /api/measurements/1/
    
    retorna la instancia de `IndicatorMeasurement` correspondiente a la medida de indicadores con índice 1.

    Los campos disponibles para cada instancia son: `epsa`, `year`, `month` y `ind1`...`ind32`, que representan la epsa, año, mes y los valores de los indicadores respectivamente.

    Los campos de la instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        /api/indicators/1/?fields=epsa,year,ind1
    
    retorna sólamente la sigla de la EPSA, el año y el valor de la variable de la instancia de `IndicatorMeasurement` con el índice 1.

    **Nota:** El campo `id` es usado en el modelo interno del sistema, por lo que no es retornado a pedidos externos.
    Para identificar de manera única una instancia `VariableReport` sin hacer uso de este campo, usamos la combinación de los campos `epsa`, `year` y `month`,
    que es garantizada de ser única entre reportes a través del proceso de validación del sistema. De esta manera el punto de acceso `list` también implementa el punto de acceso `read`. Por ejemplo,

        /api/measurements/?epsa=AAPOS&year=2017&month=6

    retorna la instancia única de medida de indicadores de la EPSA AAPOS de Junio de 2017.

    update:
    Este punto de acceso permite la edición de una instancia del modelo `IndicatorMeasurement` (medida de indicadores) que se encuentre actualmente en el sistema.

    El modelo `IndicatorMeasurement` tiene como llave primaria el campo `id` (índice de la medida de indicadores) y este campo debe ser utilizado para identificar la instancia a  editar. Por ejemplo,

        PUT /api/measurements/1/

    modificaría la instancia de `IndicatorMeasurement` con índice 1.

    El pedido HTTP debe ser del tipo `PUT` y cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `epsa`, `year`, `month` y `ind1`...`ind32`, que representan la epsa, año, mes y los valores de los indicadores respectivamente.

    Por ejemplo,

        {
            "year": <nuevo año>, 
            "ind1": <nuevo valor indicador 1>, 
            "ind2": <nuevo valor indicador 2>,
            ...
            "ind32": <nuevo valor indicador 32>,
            "epsa": <sigla de la nueva EPSA>,
            "month": <nuevo mes>
        }
    
    Reemplazaría los campos de la medida de indicadores con índice 1 por los nuevos valores. 

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será editada y el error será retornado como respuesta al pedido.

    partial_update:
    Este punto de acceso permite la edición parcial de una instancia del modelo `IndicatorMeasurement` (medida de indicadores) que se encuentre actualmente en el sistema.

    El modelo `IndicatorMeasurement` tiene como llave primaria el campo `id` (índice de la medida de indicadores) y este campo debe ser utilizado para identificar el indicador a editar. Por ejemplo,

        PATCH /api/measurements/5/

    modificaría la instancia de `IndicatorMeasurements` con el índice 5.

    El pedido HTTP debe ser del tipo `PATCH` y cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con algunos de los campos `epsa`, `year`, `month` y `ind1`...`ind32`, que representan la epsa, año, mes y los valores de los indicadores respectivamente.

    Sólamente los campos incluidos serán modificados, mientras aquellos no incluidos serán mantenidos con su valor actual.
    Por ejemplo,

        {
            "ind3": <nuevo valor de la variable 3>
        }
    
    Cambiaría sólamente el campo correspondiente al indicador 3 de la medida de indicadores con el índice 5.

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será modificada y el error será retornado como respuesta al pedido.

    delete:
    Elimina una instancia específica del modelo `IndicatorMeasurement` (medida de indicadores).

    El modelo `IndicatorMeasurement` tiene como llave primaria el campo `id` (índice de la medida de indicadores) y este campo debe ser utilizado para identificar la medida de indicadores a eliminar. Por ejemplo,

        DELETE /api/measurements/7/
    
    elimina la instancia de `IndicatorMeasurement` correspondiente a la medida de indicadores con el índice 7.

    '''
    serializer_class = serializers.IndicatorMeasurementSerializer
    queryset = models.IndicatorMeasurement.objects.all()
    filterset_fields = ('epsa','year','month',)

