from rest_framework import viewsets
from planning import models, serializers
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

class POAViewSet(CustomViewSet):
    '''
    list:
    Retorna un conjunto de instancias del modelo de planificación `POA`.
    
    Soporta los siguientes parámetros de filtro: `epsa`, `year` y `order`, que corresponden a la EPSA, el año y el orden de reprogramación del POA respectivamente. Por ejemplo,

        /api/poas/?epsa=EPSAS&year=2018
    
    retorna los POAS de EPSAS del 2018. Si ningún parámetro es dado, retorna todas las instancias disponibles.

    Los campos disponibles para cada instancia son: `epsa`, `year`, `order`, `incomes`, `expenses`, `investments` y `goals` que representan la EPSA, el año, el orden de reprogramación y las listas de ingresos, gastos, inversiones y metas de expansión del POA respectivamente.

    Al igual que las instancias, los campos de cada instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        GET /api/poas/?fields=epsa,year
    
    retorna sólamente la EPSA y el año de todas los POAs en el sistema.

    create:
    Este punto de acceso permite el ingreso de instancias del modelo de planificación `POA` al sistema.

    El pedido HTTP debe ser del tipo `POST` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `epsa`, `year`, `order`, `incomes`, `expenses`, `investments` y `goals` que representan la EPSA, el año, el orden de reprogramación y las listas de ingresos, gastos, inversiones y metas de expansión del POA respectivamente.

    La llave `incomes` es una lista de ingresos del POA y cada ingreso contiene los campos `income_type`, `description` y `value` que representan el tipo, una descripción y el valor del ingreso respectivamente.
    La llave `expenses` es una lista de gastor del POA y cada gasto contiene los campos `expense_type`, `description` y `value` que representan el tipo, una descripción y el valor del gasto respectivamente.
    La llave `investments` es una lista de inversiones del POA y cada inversión contiene los campos `description` y `value` que representan una descripción y el valor de la inversión respectivamente.
    La llave `goals` es una lista de metas de expansión del POA y cada meta contiene los campos `description`, `value`, `val_description` y `unit` que representan una descripción, el valor, una descripción del valor y la unidad de  una meta respectivamente.


    Las instancias pueden ser añadidas al sistema una a la vez o pueden ser ingresadas en masa agrupando a los objetos a ingresar en una lista en el JSON del pedido. Por ejemplo,

        [
            {
                "epsa": "EPSAS"
                "year": 2018,
                "order": 1,
                "incomes": [
                    {
                        "income_type": "otros",
                        "description": "algún ingreso",
                        "value": 9000.00
                    }
                ],
                "expenses": [
                    {
                        "expense_type": "operativos",
                        "description": "algún gasto",
                        "value": 700.50
                    }
                ],
                "investments": [ ],
                "goals": [ ],
            },{
                "epsa": "EPSAS"
                "year": 2019,
                "order": 1,
                "incomes": [ ],
                "expenses": [ ],
                "investments": [
                    {
                        "description": "algún proyecto",
                        "value": 90000
                    }
                ],
                "goals": [
                    {
                        "description": "alguna meta",
                        "value": 90
                        "val_description": ">",
                        "unit": "conex."
                    }
                ],
            }
        ]

    Añadiría dos instancias de `POA` con algunos ingresos, gastos, inversiones y metas de expansión al sistema.

    Si los objetos ingresados no pasan el proceso de validación del sistema, las instancias no serán creadas y el error será retornado como respuesta al pedido.

    read:
    Retorna una instancia específica del modelo `POA`.

    El modelo `POA` tiene como llave primaria el campo `id` (índice del POA) y este campo debe ser utilizado para identificar el POA a retornar. Por ejemplo,

        GET /api/poas/8/
    
    retorna la instancia de `POA` con índice 8.

    Los campos disponibles para cada instancia son: `epsa`, `year`, `order`, `incomes`, `expenses`, `investments` y `goals` que representan la EPSA, el año, el orden de reprogramación y las listas de ingresos, gastos, inversiones y metas de expansión del POA respectivamente.

    Los campos de la instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        GET /api/poas/8/?fields=epsa,incomes
    
    retorna sólamente la epsa y los ingresos de la instancia de `POA` con índice 8.
    
    update:
    Este punto de acceso permite la edición de una instancia del modelo `POA` que se encuentre actualmente en el sistema.

    El modelo `POA` tiene como llave primaria el campo `id` (índice del POA) y este campo debe ser utilizado para identificar la EPSA a modificar. Por ejemplo,

        PUT /api/poas/8/

    modificaría la instancia de `POA` con índice 8.

    El pedido HTTP debe ser del tipo `PUT` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos nuevos `epsa`, `year` y `order` que representan la EPSA, el año y el orden de reprogramación y del POA respectivamente.

    Por ejemplo,

        {
            "epsa": "<nueva sigla de EPSA>",
            "year": "<nuevo año>,
            "order": "<nuevo orden de reprogramación>",
        }
    
    Reemplazaría los campos del POA con índice 8 por los nuevos valores. 

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será modificada y el error será retornado como respuesta al pedido.

    Debido a la naturaleza recursiva de los campos 'incomes', 'expenses', 'investments' y 'goals' estos no pueden ser modificados utilizando este punto de acceso. Sin embargo, estos campos pueden ser modificados a través de la aplicación administrativa.
    
    partial_update:
    Este punto de acceso permite la edición de una instancia del modelo `POA` que se encuentre actualmente en el sistema.

    El modelo `POA` tiene como llave primaria el campo `id` (índice del POA) y este campo debe ser utilizado para identificar el POA a modificar. Por ejemplo,

        PATCH /api/poas/8/

    modificaría la instancia de `POA` con índice 8.

    El pedido HTTP debe ser del tipo `PATCH` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con algunos de los campos nuevos `epsa`, `year` y `order` que representan la EPSA, el año y el orden de reprogramación y del POA respectivamente.

    Por ejemplo,

        {
            "year": "<nuevo año>,
        }
    
    Reemplazaría el año del POA con índice 8 por el nuevo valor. 

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será modificada y el error será retornado como respuesta al pedido.

    Debido a la naturaleza recursiva de los campos 'incomes', 'expenses', 'investments' y 'goals' estos no puedem ser modificados utilizando este punto de acceso. Sin embargo, estos campos pueden ser modificados a través de la aplicación administrativa.
    delete:
    Elimina una instancia específica del modelo `POA`.

    El modelo `POA` tiene como llave primaria el campo `id` (índice del POA) y este campo debe ser utilizado para identificar el POA a modificar. Por ejemplo,

        DELETE /api/poas/8/

    eliminaría la instancia de `POA` con índice 8.
    '''
    serializer_class = serializers.POASerializer
    queryset = models.POA.objects.all()
    filterset_fields = ('epsa','year','order',)

class PlanViewSet(viewsets.ModelViewSet):
    '''
    list:
    Retorna un conjunto de instancias del modelo de planificación `Plan` (PDQ/PTDS).
    
    Soporta los siguientes parámetros de filtro: `epsa`, `year` y `plan_type`, que corresponden a la EPSA, el año y el tipo de plan (PDQ o PTDS) del plan respectivamente. Por ejemplo,

        GET /api/plans/?year=2018&plan_type=pdq
    
    retorna los PDQ con año inicial 2018. Si ningún parámetro es dado, retorna todas las instancias disponibles.

    Los campos disponibles para cada instancia son: `epsa`, `year`, `plan_type` y `goals` que representan la EPSA, el año, el tipo de plan(PDQ o PTDS) y las lista de metas del plan respectivamente.

    Al igual que las instancias, los campos de cada instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        GET /api/poas/?fields=epsa,goals
    
    retorna sólamente la EPSA y las metas de expansión de todas los planes en el sistema.

    create:
    Este punto de acceso permite el ingreso de instancias del modelo de planificación `Plan` (PDQ/PTDS) al sistema.

    El pedido HTTP debe ser del tipo `POST` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos `epsa`, `year`, `plan_type` y `goals` que representan la EPSA, el año, el tipo de plan(PDQ o PTDS) y las lista de metas del plan respectivamente.
    
    La llave `goals` es una lista de metas de expansión del plan y cada meta contiene los campos `year`, `description`, `value`, `val_description` y `unit` que representan el año, una descripción, el valor, una descripción del valor y la unidad de  una meta respectivamente.


    Las instancias pueden ser añadidas al sistema una a la vez o pueden ser ingresadas en masa agrupando a los objetos a ingresar en una lista en el JSON del pedido. Por ejemplo,

        [
            {
                "epsa": "EPSAS"
                "year": 2018,
                "plan_type": "pdq",
                "goals": [ ],
            },{
                "epsa": "SAGUAPAC"
                "year": 2019,
                "plan_type": "pdq",
                "goals": [
                    {
                        "year": 2019,
                        "description": "alguna meta",
                        "value": 90
                        "val_description": ">",
                        "unit": "conex."
                    },{
                        "year": 2020,
                        "description": "alguna meta",
                        "value": 100
                        "val_description": ">",
                        "unit": "conex."

                    }
                ],
            }
        ]

    Añadiría dos instancias de `Plan` con algunas metas de expansión al sistema.

    Si los objetos ingresados no pasan el proceso de validación del sistema, las instancias no serán creadas y el error será retornado como respuesta al pedido.

    read:
    Retorna una instancia específica del modelo de planificación `Plan` (PDQ/PTDS) al sistema.

    El modelo `Plan` tiene como llave primaria el campo `id` (índice del PDQ/PTDS) y este campo debe ser utilizado para identificar el Plan a retornar. Por ejemplo,

        GET /api/plans/8/
    
    retorna la instancia de `Plan` con índice 8.

    Los campos disponibles para cada instancia son: `epsa`, `year`, `plan_type` y `goals` que representan la EPSA, el año, el tipo de plan(PDQ o PTDS) y las lista de metas del plan respectivamente.

    Los campos de la instancia retornada pueden ser filtrados añadiendo el parámetro `fields`.  Por ejemplo,

        GET /api/plans/8/?fields=epsa,goals
    
    retorna sólamente la epsa y las metas de expansión de la instancia de `Plan` con índice 8.
    
    update:
    Este punto de acceso permite la edición de una instancia del modelo de planificación `Plan` (PDQ/PTDS) que se encuentre en el sistema.

    El modelo `Plan` tiene como llave primaria el campo `id` (índice del PDQ/PTDS) y este campo debe ser utilizado para identificar el Plan a retornar. Por ejemplo,

        PUT /api/plans/8/
    
    modificaría la instancia de `Plan` con índice 8.
    
    El pedido HTTP debe ser del tipo `PUT` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con los campos nuevos `epsa`, `year` y `plan_type` que representan la EPSA, el año y el tipo de plan(PDQ o PTDS) del plan respectivamente.

    Por ejemplo,

        {
            "epsa": "<nueva sigla de EPSA>",
            "year": "<nuevo año>,
            "plan_type": "<nuevo tipo de plan>",
        }
    
    Reemplazaría los campos del plan con índice 8 por los nuevos valores. 

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será modificada y el error será retornado como respuesta al pedido.

    Debido a la naturaleza recursiva del campo 'goals' este no puede ser modificado utilizando este punto de acceso. Sin embargo, este campo puede ser modificado a través de la aplicación administrativa.
    
    partial_update:
    Este punto de acceso permite la edición parcial de una instancia del modelo de planificación `Plan` (PDQ/PTDS) que se encuentre en el sistema.

    El modelo `Plan` tiene como llave primaria el campo `id` (índice del PDQ/PTDS) y este campo debe ser utilizado para identificar el Plan a retornar. Por ejemplo,

        PATCH /api/plans/8/
    
    modificaría la instancia de `Plan` con índice 8.
    
    El pedido HTTP debe ser del tipo `PATCH` y el cuerpo del pedido debe ser un objeto codificado del tipo `application/json` con algunos de los campos nuevos `epsa`, `year` y `plan_type` que representan la EPSA, el año y el tipo de plan(PDQ o PTDS) del plan respectivamente.

    Por ejemplo,

        {
            "year": "<nuevo año>,
        }
    
    Reemplazaría el año plan con índice 8 por el nuevo valor. 

    Si los campos ingresados no pasan el proceso de validación del sistema, las instancia no será modificada y el error será retornado como respuesta al pedido.

    Debido a la naturaleza recursiva del campo 'goals' este no puede ser modificado utilizando este punto de acceso. Sin embargo, este campo puede ser modificado a través de la aplicación administrativa.
    delete:
    Elimina una instancia específica del modelo de planificación `Plan` (PDQ/PTDS) que se encuentre en el sistema.

    El modelo `Plan` tiene como llave primaria el campo `id` (índice del PDQ/PTDS) y este campo debe ser utilizado para identificar el Plan a retornar. Por ejemplo,

        DELETE /api/plans/8/
    
    eliminaría la instancia de `Plan` con índice 8.
    '''
    serializer_class = serializers.PlanSerializer
    queryset = models.Plan.objects.all()
    filterset_fields = ('epsa','year','plan_type',)


    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(PlanViewSet, self).get_serializer(*args, **kwargs)
