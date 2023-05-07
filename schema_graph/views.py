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

        abstract_models = schema.abstract_models
        models = schema.models
        foreign_keys = schema.foreign_keys
        many_to_manys = schema.many_to_manys
        one_to_ones = schema.one_to_ones
        inheritance = schema.inheritance
        proxies = schema.proxies

        kwargs.update(
            {
                "abstract_models": json.dumps(abstract_models),
                "models": json.dumps(models),
                "foreign_keys": json.dumps(foreign_keys),
                "many_to_manys": json.dumps(many_to_manys),
                "one_to_ones": json.dumps(one_to_ones),
                "inheritance": json.dumps(inheritance),
                "proxies": json.dumps(proxies),
            }
        )
        return super().get_context_data(**kwargs)
