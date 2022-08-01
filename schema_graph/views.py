import json

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView

from schema_graph.schema import get_schema


class Schema(TemplateView):
    template_name = "schema_graph/schema.html"

    def dispatch(self, request):
        if not settings.DEBUG:
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
