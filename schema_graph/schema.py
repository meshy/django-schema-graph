from collections import defaultdict

from attr import attrib, attrs
from django.apps import apps


@attrs
class Schema(object):
    # Vertices
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


def get_model_id(model, app=None):
    if not app:
        app = apps.get_app_config(model._meta.app_label)

    return (app.name, model.__name__)


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


def get_schema():
    nodes = defaultdict(tuple)
    foreign_keys = []
    one_to_one = []
    many_to_many = []
    inheritance = []
    proxy = []

    for app, model in get_app_models():
        app_label, model_name = model_id = get_model_id(model, app)
        nodes[app_label] += (model_name,)

        # Proxy models
        if model._meta.proxy:
            related_model_id = get_model_id(model._meta.proxy_for_model)
            relationship = (model_id, related_model_id)
            proxy.append(relationship)
            continue

        # Subclassing
        if model._meta.parents:
            for parent_model in model._meta.parents:
                parent_model_id = get_model_id(parent_model)
                relationship = model_id, parent_model_id
                inheritance.append(relationship)

        # Fields
        fks, o2o, m2m = get_field_relationships(model)
        foreign_keys.extend(fks)
        one_to_one.extend(o2o)
        many_to_many.extend(m2m)

    for app_label in nodes:
        nodes[app_label] = tuple(sorted(nodes[app_label]))

    return Schema(
        # Vertices
        models=dict(nodes),
        proxies=sorted(proxy),
        # Edges
        foreign_keys=sorted(foreign_keys),
        inheritance=sorted(inheritance),
        many_to_manys=sorted(many_to_many),
        one_to_ones=sorted(one_to_one),
    )
