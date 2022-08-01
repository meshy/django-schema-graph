import json

import pytest
from django.http import Http404
from django.test import RequestFactory, override_settings

from schema_graph.schema import get_schema
from schema_graph.views import Schema


def create_request():
    return RequestFactory().get("/ignored/")


def test_context():
    """The schema should be available in the template context."""
    request = create_request()
    view = Schema(request=request)
    context = view.get_context_data()
    schema = get_schema()
    assert context["models"] == json.dumps(schema.models)
    assert context["foreign_keys"] == json.dumps(schema.foreign_keys)
    assert context["many_to_manys"] == json.dumps(schema.many_to_manys)
    assert context["one_to_ones"] == json.dumps(schema.one_to_ones)
    assert context["inheritance"] == json.dumps(schema.inheritance)
    assert context["proxies"] == json.dumps(schema.proxies)


def test_content():
    """The page should be rendered."""
    view = Schema.as_view()
    request = create_request()
    with override_settings(DEBUG=True):
        response = view(request)

    assert response.rendered_content.startswith("<!doctype html>")


@pytest.mark.parametrize(
    "settings_dict",
    [
        # SCHEMA_GRAPH_VISIBLE takes priority over DEBUG.
        {"DEBUG": True, "SCHEMA_GRAPH_VISIBLE": True},
        {"DEBUG": False, "SCHEMA_GRAPH_VISIBLE": True},
        {"DEBUG": True},
    ],
)
def test_accessible_settings(settings_dict):
    view = Schema.as_view()
    request = create_request()
    with override_settings(**settings_dict):
        response = view(request)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "settings_dict",
    [
        # SCHEMA_GRAPH_VISIBLE takes priority over DEBUG.
        {"DEBUG": True, "SCHEMA_GRAPH_VISIBLE": False},
        {"DEBUG": False, "SCHEMA_GRAPH_VISIBLE": False},
        {"DEBUG": False},
    ],
)
def test_inaccessible_settings(settings_dict):
    view = Schema.as_view()
    request = create_request()
    with override_settings(**settings_dict):
        with pytest.raises(Http404):
            view(request)
