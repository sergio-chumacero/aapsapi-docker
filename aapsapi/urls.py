from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from supply_areas.views import SupplyAreaViewSet
from ambiental.views import SARHViewSet
from performance import views as performance_views
from planning import views as planning_views

from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

admin.site.site_url = None

schema_view = get_schema_view(
   openapi.Info(
      title="AAPS API",
      default_version='v1',
      description="API privada - Diseñada para ofrecer puntos de acceso al sistema de información de la AAPS (Bolivia).",
    #   terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="sergio.chumacero.fi@gmail.com"),
    #   license=openapi.License(name="No especificada"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register('supply_areas', SupplyAreaViewSet, basename='supply_areas')
router.register('sarhs',SARHViewSet,basename='sarhs')
router.register('epsas', performance_views.EPSAViewSet)
router.register('variables', performance_views.VariableViewSet)
router.register('indicators', performance_views.IndicatorViewSet)
router.register('reports', performance_views.VariableReportViewSet)
router.register('measurements', performance_views.IndicatorMeasurementViewSet)
router.register('poas', planning_views.POAViewSet)
router.register('plans', planning_views.PlanViewSet)

docs_description ='''
Sistema REST API privado de la AAPS. 
Ofrece puntos de acceso a datos de EPSA, Variables, Indicadores, POAs, PDQs, PTDs y áreas de cobertura de las EPSA reguladas.
Esta página muestra los puntos de acceso y su uso de manera interactiva. 
Desde acá, es posible explorar y realizar pedidos al sistema.

Los pedidos al sistema deben contar con credenciales de autenticación básica o un header llamado "Authorization" con el Token de autenticación proveido por el sistema, por ejemplo,

    Authorization: Token <Token proveido por el sistema>

Los Tokens de autenticación son proevidos por el sistema a través del punto de acceso `/api-token-auth/` descrito en esta documentación.

La especificación del tipo "Swagger":

[https://aaps-data.appspot.com/swagger](https://aaps-data.appspot.com/swagger/) 

ofrece más información acerca de los modelos de datos del sistema.
'''

docs_view = include_docs_urls(
    title='AAPS-API',
    description=docs_description,
    public=True,
    permission_classes=[permissions.AllowAny,]
)


urlpatterns = [
    path('', RedirectView.as_view(url='/admin/')),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token),

    path('docs/', docs_view),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
