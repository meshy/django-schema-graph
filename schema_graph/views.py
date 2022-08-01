import json

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
        kwargs.update(
            {
                "abstract_models": json.dumps(schema.abstract_models),
                "models": json.dumps(schema.models),
                "foreign_keys": json.dumps(schema.foreign_keys),
                "many_to_manys": json.dumps(schema.many_to_manys),
                "one_to_ones": json.dumps(schema.one_to_ones),
                "inheritance": json.dumps(schema.inheritance),
                "proxies": json.dumps(schema.proxies),
            }
        )
        return super(Schema, self).get_context_data(**kwargs)
