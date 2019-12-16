from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(modules.LinkList(
            _('REST API'),
            children=[
                {
                    'title': _('Documentación API'),
                    'url': 'https://aaps-data.appspot.com/docs/',
                    'external': True,
                },
                {
                    'title': _('Documentación Swagger'),
                    'url': 'https://aaps-data.appspot.com/swagger/',
                    'external': True,
                },
            ],
            column=1,
            order=0
        ))
        self.children.append(modules.AppList(
            _('Aplicaciones'),
            column=0,
            order=0
        ))
        self.children.append(modules.RecentActions(
            _('Acciones Recientes'),
            column=2,
            order=0
        ))