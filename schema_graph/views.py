from cattrs.preconf.json import make_converter as make_json_converter
from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView

from schema_graph.schema import get_schema


class Schema(TemplateView):
    template_name = "schema_graph/schema.html"

    def access_permitted(self):
        """
        When this returns True, the schema graph page is accessible.

        We look for the setting `SCHEMA_GRAPH_VISIBLE`, and fall back to `DEBUG`.

        To control this on a per-request basis, override this function in a subclass.
        The request will be accessible using `self.request`.
        """

        return getattr(settings, "SCHEMA_GRAPH_VISIBLE", settings.DEBUG)

    def dispatch(self, request):
        if not self.access_permitted():
            raise Http404()
        return super().dispatch(request)

    def get_context_data(self, **kwargs):
        schema = get_schema()
        json_converter = make_json_converter()
        kwargs["schema"] = json_converter.dumps(schema)
        return super().get_context_data(**kwargs)
