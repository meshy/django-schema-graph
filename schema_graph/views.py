import json

from django.conf import settings
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from schema_graph.schema import get_schema


def debug_required(view_function):
    def view_wrapper(request, *args, **kwargs):
        if not settings.DEBUG:
            raise Http404()
        return view_function(request, *args, **kwargs)

    return view_wrapper


class Schema(TemplateView):
    template_name = "schema_graph/schema.html"

    @method_decorator(debug_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Schema, self).dispatch(request, *args, **kwargs)

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
