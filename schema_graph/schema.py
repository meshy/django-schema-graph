from collections import defaultdict

from attr import attrib, attrs
from django.apps import apps
from django.db import models


@attrs
class Schema(object):
    # Vertices
    abstract_models = attrib()
    models = attrib()
    proxies = attrib()
    # Edges
    foreign_keys = attrib()
    inheritance = attrib()
    many_to_manys = attrib()
    one_to_ones = attrib()


def get_app_models():
    for app in apps.get_app_configs():
        for model in app.get_models():
            yield app, model


def get_model_id(model):
    app_label = model._meta.app_label
    try:
        app_name = apps.get_app_config(app_label).name
    except LookupError:
        app_name = model.__module__

    return (app_name, model.__name__)


def get_field_relationships(model):
    foreign_keys = []
    one_to_one = []
    many_to_many = []

    model_id = get_model_id(model)

    for field in model._meta.get_fields():
        # Ignore non-relation fields
        if not field.is_relation:
            continue
        # Skip fields defined on superclasses
        if field.model != model:
            continue
        related_model = field.related_model
        # GenericForeignKey
        if related_model is None:
            continue
        related_model_id = get_model_id(related_model)
        relationship = (model_id, related_model_id)
        # Foreign key
        if field.many_to_one:
            foreign_keys.append(relationship)
        # One-to-one
        elif field.one_to_one and not field.auto_created:
            one_to_one.append(relationship)
        # Many-to-many
        elif field.many_to_many and not field.auto_created:
            many_to_many.append(relationship)

    return foreign_keys, one_to_one, many_to_many


def is_model_subclass(obj):
    if obj is models.Model:
        return False
    return issubclass(obj, models.Model)


def get_schema():
    abstract_nodes = defaultdict(set)
    nodes = defaultdict(tuple)
    foreign_keys = []
    one_to_one = []
    many_to_many = []
    inheritance = set()
    proxy = []

    for app, model in get_app_models():
        app_label, model_name = model_id = get_model_id(model)
        nodes[app_label] += (model_name,)

        # Proxy models
        if model._meta.proxy:
            related_model_id = get_model_id(model._meta.proxy_for_model)
            relationship = (model_id, related_model_id)
            proxy.append(relationship)
            continue

        # Subclassing
        for base in filter(is_model_subclass, model.__mro__):
            base_app_label, base_model_name = get_model_id(base)
            if base._meta.abstract:
                abstract_nodes[base_app_label].add(base_model_name)
            for parent in filter(is_model_subclass, base.__bases__):
                inheritance.add(
                    ((base_app_label, base_model_name), get_model_id(parent))
                )

        # Fields
        fks, o2o, m2m = get_field_relationships(model)
        foreign_keys.extend(fks)
        one_to_one.extend(o2o)
        many_to_many.extend(m2m)

    for app_label in nodes:
        nodes[app_label] = tuple(sorted(nodes[app_label]))

    for app_label in abstract_nodes:
        abstract_nodes[app_label] = tuple(sorted(abstract_nodes[app_label]))

    return Schema(
        # Vertices
        abstract_models=dict(abstract_nodes),
        models=dict(nodes),
        proxies=sorted(proxy),
        # Edges
        foreign_keys=sorted(foreign_keys),
        inheritance=sorted(inheritance),
        many_to_manys=sorted(many_to_many),
        one_to_ones=sorted(one_to_one),
    )
