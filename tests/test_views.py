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

    assert json.loads(context["schema"]) == {
        "nodes": [
            {
                "id": "django.contrib.auth.base_user.AbstractBaseUser",
                "name": "AbstractBaseUser",
                "group": "django.contrib.auth",
                "tags": ["abstract"],
            },
            {
                "id": "django.contrib.auth.models.AbstractUser",
                "name": "AbstractUser",
                "group": "django.contrib.auth",
                "tags": ["abstract"],
            },
            {
                "id": "django.contrib.auth.models.Group",
                "name": "Group",
                "group": "django.contrib.auth",
                "tags": [],
            },
            {
                "id": "django.contrib.auth.models.Permission",
                "name": "Permission",
                "group": "django.contrib.auth",
                "tags": [],
            },
            {
                "id": "django.contrib.auth.models.PermissionsMixin",
                "name": "PermissionsMixin",
                "group": "django.contrib.auth",
                "tags": ["abstract"],
            },
            {
                "id": "django.contrib.auth.models.User",
                "name": "User",
                "group": "django.contrib.auth",
                "tags": [],
            },
            {
                "id": "django.contrib.contenttypes.models.ContentType",
                "name": "ContentType",
                "group": "django.contrib.contenttypes",
                "tags": [],
            },
            {
                "id": "django.contrib.sessions.base_session.AbstractBaseSession",
                "name": "AbstractBaseSession",
                "group": "django.contrib.sessions",
                "tags": ["abstract"],
            },
            {
                "id": "django.contrib.sessions.models.Session",
                "name": "Session",
                "group": "django.contrib.sessions",
                "tags": [],
            },
            {
                "id": "django.contrib.sites.models.Site",
                "name": "Site",
                "group": "django.contrib.sites",
                "tags": [],
            },
            {
                "id": "tests.app_a.models.InterAppSubclass",
                "name": "InterAppSubclass",
                "group": "tests.app_a",
                "tags": [],
            },
            {
                "id": "tests.app_b.models.InterAppForeignKey",
                "name": "InterAppForeignKey",
                "group": "tests.app_b",
                "tags": [],
            },
            {
                "id": "tests.app_c.models.InterAppOneToOne",
                "name": "InterAppOneToOne",
                "group": "tests.app_c",
                "tags": [],
            },
            {
                "id": "tests.app_d.models.InterAppManyToMany",
                "name": "InterAppManyToMany",
                "group": "tests.app_d",
                "tags": [],
            },
            {
                "id": "tests.app_d.models.InterAppProxy",
                "name": "InterAppProxy",
                "group": "tests.app_d",
                "tags": ["proxy"],
            },
            {
                "id": "tests.basic.models.ManyToManyWithThroughTable",
                "name": "ManyToManyWithThroughTable",
                "group": "tests.basic",
                "tags": [],
            },
            {
                "id": "tests.basic.models.OutgoingForeignKey",
                "name": "OutgoingForeignKey",
                "group": "tests.basic",
                "tags": [],
            },
            {
                "id": "tests.basic.models.OutgoingManyToMany",
                "name": "OutgoingManyToMany",
                "group": "tests.basic",
                "tags": [],
            },
            {
                "id": "tests.basic.models.OutgoingOneToOne",
                "name": "OutgoingOneToOne",
                "group": "tests.basic",
                "tags": [],
            },
            {
                "id": "tests.basic.models.SelfReference",
                "name": "SelfReference",
                "group": "tests.basic",
                "tags": [],
            },
            {
                "id": "tests.basic.models.Target",
                "name": "Target",
                "group": "tests.basic",
                "tags": [],
            },
            {
                "id": "tests.basic.models.ThroughTable",
                "name": "ThroughTable",
                "group": "tests.basic",
                "tags": [],
            },
            {
                "id": "tests.generic.models.GenericFK",
                "name": "GenericFK",
                "group": "tests.generic",
                "tags": [],
            },
            {
                "id": "tests.inheritance.models.Abstract",
                "name": "Abstract",
                "group": "tests.inheritance",
                "tags": ["abstract"],
            },
            {
                "id": "tests.inheritance.models.AbstractBase",
                "name": "AbstractBase",
                "group": "tests.inheritance",
                "tags": ["abstract"],
            },
            {
                "id": "tests.inheritance.models.AbstractMultipleInheritance",
                "name": "AbstractMultipleInheritance",
                "group": "tests.inheritance",
                "tags": [],
            },
            {
                "id": "tests.inheritance.models.AbstractSubclass1",
                "name": "AbstractSubclass1",
                "group": "tests.inheritance",
                "tags": ["abstract"],
            },
            {
                "id": "tests.inheritance.models.AbstractSubclass2",
                "name": "AbstractSubclass2",
                "group": "tests.inheritance",
                "tags": ["abstract"],
            },
            {
                "id": "tests.inheritance.models.Concrete",
                "name": "Concrete",
                "group": "tests.inheritance",
                "tags": [],
            },
            {
                "id": "tests.inheritance.models.ConcreteBase",
                "name": "ConcreteBase",
                "group": "tests.inheritance",
                "tags": [],
            },
            {
                "id": "tests.inheritance.models.ConcreteInheritance",
                "name": "ConcreteInheritance",
                "group": "tests.inheritance",
                "tags": [],
            },
            {
                "id": "tests.inheritance.models.ConcreteSubclass1",
                "name": "ConcreteSubclass1",
                "group": "tests.inheritance",
                "tags": [],
            },
            {
                "id": "tests.inheritance.models.ConcreteSubclass2",
                "name": "ConcreteSubclass2",
                "group": "tests.inheritance",
                "tags": [],
            },
            {
                "id": "tests.inheritance.models.MixedMultipleInheritance",
                "name": "MixedMultipleInheritance",
                "group": "tests.inheritance",
                "tags": [],
            },
            {
                "id": "tests.inheritance.models.SubSubclass",
                "name": "SubSubclass",
                "group": "tests.inheritance",
                "tags": [],
            },
            {
                "id": "tests.inheritance.models.Subclass",
                "name": "Subclass",
                "group": "tests.inheritance",
                "tags": [],
            },
            {
                "id": "tests.installed.models.ConcreteInstalled",
                "name": "ConcreteInstalled",
                "group": "tests.installed",
                "tags": [],
            },
            {
                "id": "tests.not_installed.models.AbstractNotInstalled",
                "name": "AbstractNotInstalled",
                "group": "tests.not_installed.models",
                "tags": ["abstract"],
            },
            {
                "id": "tests.proxy.models.ProxyNode",
                "name": "ProxyNode",
                "group": "tests.proxy",
                "tags": ["proxy"],
            },
            {
                "id": "tests.proxy.models.ProxyNode2",
                "name": "ProxyNode2",
                "group": "tests.proxy",
                "tags": ["proxy"],
            },
            {
                "id": "tests.proxy.models.Target",
                "name": "Target",
                "group": "tests.proxy",
                "tags": [],
            },
        ],
        "edges": [
            {
                "source": "django.contrib.auth.models.AbstractUser",
                "target": "django.contrib.auth.base_user.AbstractBaseUser",
                "tags": ["subclass"],
            },
            {
                "source": "django.contrib.auth.models.AbstractUser",
                "target": "django.contrib.auth.models.PermissionsMixin",
                "tags": ["subclass"],
            },
            {
                "source": "django.contrib.auth.models.Group",
                "target": "django.contrib.auth.models.Permission",
                "tags": ["many-to-many"],
            },
            {
                "source": "django.contrib.auth.models.Permission",
                "target": "django.contrib.contenttypes.models.ContentType",
                "tags": ["foreign-key"],
            },
            {
                "source": "django.contrib.auth.models.User",
                "target": "django.contrib.auth.models.AbstractUser",
                "tags": ["subclass"],
            },
            {
                "source": "django.contrib.auth.models.User",
                "target": "django.contrib.auth.models.Group",
                "tags": ["many-to-many"],
            },
            {
                "source": "django.contrib.auth.models.User",
                "target": "django.contrib.auth.models.Permission",
                "tags": ["many-to-many"],
            },
            {
                "source": "django.contrib.sessions.models.Session",
                "target": "django.contrib.sessions.base_session.AbstractBaseSession",
                "tags": ["subclass"],
            },
            {
                "source": "tests.app_a.models.InterAppSubclass",
                "target": "django.contrib.auth.models.Group",
                "tags": ["subclass"],
            },
            {
                "source": "tests.app_b.models.InterAppForeignKey",
                "target": "django.contrib.auth.models.User",
                "tags": ["foreign-key"],
            },
            {
                "source": "tests.app_c.models.InterAppOneToOne",
                "target": "tests.app_b.models.InterAppForeignKey",
                "tags": ["one-to-one"],
            },
            {
                "source": "tests.app_d.models.InterAppManyToMany",
                "target": "tests.app_b.models.InterAppForeignKey",
                "tags": ["many-to-many"],
            },
            {
                "source": "tests.app_d.models.InterAppProxy",
                "target": "tests.app_c.models.InterAppOneToOne",
                "tags": ["proxy"],
            },
            {
                "source": "tests.basic.models.OutgoingForeignKey",
                "target": "tests.basic.models.Target",
                "tags": ["foreign-key"],
            },
            {
                "source": "tests.basic.models.OutgoingManyToMany",
                "target": "tests.basic.models.Target",
                "tags": ["many-to-many"],
            },
            {
                "source": "tests.basic.models.OutgoingOneToOne",
                "target": "tests.basic.models.Target",
                "tags": ["one-to-one"],
            },
            {
                "source": "tests.basic.models.SelfReference",
                "target": "tests.basic.models.SelfReference",
                "tags": ["foreign-key"],
            },
            {
                "source": "tests.basic.models.ThroughTable",
                "target": "tests.basic.models.ManyToManyWithThroughTable",
                "tags": ["foreign-key"],
            },
            {
                "source": "tests.basic.models.ThroughTable",
                "target": "tests.basic.models.Target",
                "tags": ["foreign-key"],
            },
            {
                "source": "tests.generic.models.GenericFK",
                "target": "django.contrib.contenttypes.models.ContentType",
                "tags": ["foreign-key"],
            },
            {
                "source": "tests.inheritance.models.AbstractMultipleInheritance",
                "target": "tests.inheritance.models.AbstractSubclass1",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.AbstractMultipleInheritance",
                "target": "tests.inheritance.models.AbstractSubclass2",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.AbstractSubclass1",
                "target": "tests.inheritance.models.AbstractBase",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.AbstractSubclass2",
                "target": "tests.inheritance.models.AbstractBase",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.Concrete",
                "target": "tests.inheritance.models.Abstract",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.ConcreteInheritance",
                "target": "tests.inheritance.models.ConcreteSubclass1",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.ConcreteInheritance",
                "target": "tests.inheritance.models.ConcreteSubclass2",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.ConcreteSubclass1",
                "target": "tests.inheritance.models.ConcreteBase",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.ConcreteSubclass2",
                "target": "tests.inheritance.models.ConcreteBase",
                "tags": ["one-to-one"],
            },
            {
                "source": "tests.inheritance.models.ConcreteSubclass2",
                "target": "tests.inheritance.models.ConcreteBase",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.MixedMultipleInheritance",
                "target": "tests.inheritance.models.AbstractBase",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.MixedMultipleInheritance",
                "target": "tests.inheritance.models.ConcreteBase",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.SubSubclass",
                "target": "tests.inheritance.models.Subclass",
                "tags": ["subclass"],
            },
            {
                "source": "tests.inheritance.models.Subclass",
                "target": "tests.inheritance.models.ConcreteBase",
                "tags": ["subclass"],
            },
            {
                "source": "tests.installed.models.ConcreteInstalled",
                "target": "tests.not_installed.models.AbstractNotInstalled",
                "tags": ["subclass"],
            },
            {
                "source": "tests.proxy.models.ProxyNode",
                "target": "tests.proxy.models.Target",
                "tags": ["proxy"],
            },
            {
                "source": "tests.proxy.models.ProxyNode2",
                "target": "tests.proxy.models.Target",
                "tags": ["proxy"],
            },
        ],
        "groups": [
            {"id": "django.contrib.auth", "name": "django.contrib.auth"},
            {
                "id": "django.contrib.contenttypes",
                "name": "django.contrib.contenttypes",
            },
            {"id": "django.contrib.sessions", "name": "django.contrib.sessions"},
            {"id": "django.contrib.sites", "name": "django.contrib.sites"},
            {"id": "tests.app_a", "name": "tests.app_a"},
            {"id": "tests.app_b", "name": "tests.app_b"},
            {"id": "tests.app_c", "name": "tests.app_c"},
            {"id": "tests.app_d", "name": "tests.app_d"},
            {"id": "tests.basic", "name": "tests.basic"},
            {"id": "tests.generic", "name": "tests.generic"},
            {"id": "tests.inheritance", "name": "tests.inheritance"},
            {"id": "tests.installed", "name": "tests.installed"},
            {"id": "tests.not_installed.models", "name": "tests.not_installed.models"},
            {"id": "tests.proxy", "name": "tests.proxy"},
        ],
    }


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
