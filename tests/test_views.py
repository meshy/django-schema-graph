import json

import pytest
from django.http import Http404
from django.test import RequestFactory, override_settings

from schema_graph.views import Schema


def create_request():
    return RequestFactory().get("/ignored/")


def test_context():
    """The schema should be available in the template context."""
    request = create_request()
    view = Schema(request=request)
    context = view.get_context_data()
    assert json.loads(context["abstract_models"]) == {
        "django.contrib.auth": ["AbstractBaseUser", "AbstractUser", "PermissionsMixin"],
        "django.contrib.sessions": ["AbstractBaseSession"],
        "tests.inheritance": [
            "Abstract",
            "AbstractBase",
            "AbstractSubclass1",
            "AbstractSubclass2",
        ],
        "tests.not_installed.models": ["AbstractNotInstalled"],
    }
    assert json.loads(context["models"]) == {
        "django.contrib.auth": ["Group", "Permission", "User"],
        "django.contrib.contenttypes": ["ContentType"],
        "django.contrib.sessions": ["Session"],
        "django.contrib.sites": ["Site"],
        "tests.app_a": ["InterAppSubclass"],
        "tests.app_b": ["InterAppForeignKey"],
        "tests.app_c": ["InterAppOneToOne"],
        "tests.app_d": ["InterAppManyToMany", "InterAppProxy"],
        "tests.basic": [
            "ManyToManyWithThroughTable",
            "OutgoingForeignKey",
            "OutgoingManyToMany",
            "OutgoingOneToOne",
            "SelfReference",
            "Target",
            "ThroughTable",
        ],
        "tests.generic": ["GenericFK"],
        "tests.inheritance": [
            "AbstractMultipleInheritance",
            "Concrete",
            "ConcreteBase",
            "ConcreteInheritance",
            "ConcreteSubclass1",
            "ConcreteSubclass2",
            "MixedMultipleInheritance",
            "SubSubclass",
            "Subclass",
        ],
        "tests.installed": ["ConcreteInstalled"],
        "tests.proxy": ["ProxyNode", "ProxyNode2", "Target"],
    }
    assert json.loads(context["foreign_keys"]) == [
        [
            ["django.contrib.auth", "Permission"],
            ["django.contrib.contenttypes", "ContentType"],
        ],
        [["tests.app_b", "InterAppForeignKey"], ["django.contrib.auth", "User"]],
        [["tests.basic", "OutgoingForeignKey"], ["tests.basic", "Target"]],
        [["tests.basic", "SelfReference"], ["tests.basic", "SelfReference"]],
        [
            ["tests.basic", "ThroughTable"],
            ["tests.basic", "ManyToManyWithThroughTable"],
        ],
        [["tests.basic", "ThroughTable"], ["tests.basic", "Target"]],
        [
            ["tests.generic", "GenericFK"],
            ["django.contrib.contenttypes", "ContentType"],
        ],
    ]
    assert json.loads(context["many_to_manys"]) == [
        [["django.contrib.auth", "Group"], ["django.contrib.auth", "Permission"]],
        [["django.contrib.auth", "User"], ["django.contrib.auth", "Group"]],
        [["django.contrib.auth", "User"], ["django.contrib.auth", "Permission"]],
        [["tests.app_d", "InterAppManyToMany"], ["tests.app_b", "InterAppForeignKey"]],
        [["tests.basic", "OutgoingManyToMany"], ["tests.basic", "Target"]],
    ]
    assert json.loads(context["one_to_ones"]) == [
        [["tests.app_c", "InterAppOneToOne"], ["tests.app_b", "InterAppForeignKey"]],
        [["tests.basic", "OutgoingOneToOne"], ["tests.basic", "Target"]],
        [
            ["tests.inheritance", "ConcreteSubclass2"],
            ["tests.inheritance", "ConcreteBase"],
        ],
    ]
    assert json.loads(context["inheritance"]) == [
        [
            ["django.contrib.auth", "AbstractUser"],
            ["django.contrib.auth", "AbstractBaseUser"],
        ],
        [
            ["django.contrib.auth", "AbstractUser"],
            ["django.contrib.auth", "PermissionsMixin"],
        ],
        [["django.contrib.auth", "User"], ["django.contrib.auth", "AbstractUser"]],
        [
            ["django.contrib.sessions", "Session"],
            ["django.contrib.sessions", "AbstractBaseSession"],
        ],
        [["tests.app_a", "InterAppSubclass"], ["django.contrib.auth", "Group"]],
        [
            ["tests.inheritance", "AbstractMultipleInheritance"],
            ["tests.inheritance", "AbstractSubclass1"],
        ],
        [
            ["tests.inheritance", "AbstractMultipleInheritance"],
            ["tests.inheritance", "AbstractSubclass2"],
        ],
        [
            ["tests.inheritance", "AbstractSubclass1"],
            ["tests.inheritance", "AbstractBase"],
        ],
        [
            ["tests.inheritance", "AbstractSubclass2"],
            ["tests.inheritance", "AbstractBase"],
        ],
        [["tests.inheritance", "Concrete"], ["tests.inheritance", "Abstract"]],
        [
            ["tests.inheritance", "ConcreteInheritance"],
            ["tests.inheritance", "ConcreteSubclass1"],
        ],
        [
            ["tests.inheritance", "ConcreteInheritance"],
            ["tests.inheritance", "ConcreteSubclass2"],
        ],
        [
            ["tests.inheritance", "ConcreteSubclass1"],
            ["tests.inheritance", "ConcreteBase"],
        ],
        [
            ["tests.inheritance", "ConcreteSubclass2"],
            ["tests.inheritance", "ConcreteBase"],
        ],
        [
            ["tests.inheritance", "MixedMultipleInheritance"],
            ["tests.inheritance", "AbstractBase"],
        ],
        [
            ["tests.inheritance", "MixedMultipleInheritance"],
            ["tests.inheritance", "ConcreteBase"],
        ],
        [["tests.inheritance", "SubSubclass"], ["tests.inheritance", "Subclass"]],
        [["tests.inheritance", "Subclass"], ["tests.inheritance", "ConcreteBase"]],
        [
            ["tests.installed", "ConcreteInstalled"],
            ["tests.not_installed.models", "AbstractNotInstalled"],
        ],
    ]
    assert json.loads(context["proxies"]) == [
        [["tests.app_d", "InterAppProxy"], ["tests.app_c", "InterAppOneToOne"]],
        [["tests.proxy", "ProxyNode"], ["tests.proxy", "Target"]],
        [["tests.proxy", "ProxyNode2"], ["tests.proxy", "Target"]],
    ]


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
