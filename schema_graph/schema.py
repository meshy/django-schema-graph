from __future__ import annotations

from collections.abc import Iterator

import attrs
from django import apps
from django.db import models


@attrs.frozen(order=True)
class Node:
    id: str
    name: str
    group: str
    tags: tuple[str, ...] = ()

    @classmethod
    def from_model(cls, model: type[models.Model]) -> Node:
        tags = []
        if model._meta.proxy:
            tags.append("proxy")
        if model._meta.abstract:
            tags.append("abstract")
        return cls(
            id=get_model_id(model),
            name=model.__name__,
            group=get_app_name(model),
            tags=tuple(tags),
        )


@attrs.frozen(order=True)
class Edge:
    source: str
    target: str
    tags: tuple[str, ...] = ()

    @classmethod
    def proxy(cls, child: type[models.Model], parent: type[models.Model]) -> Edge:
        return cls(get_model_id(child), get_model_id(parent), tags=("proxy",))

    @classmethod
    def subclass(cls, child: type[models.Model], parent: type[models.Model]) -> Edge:
        return cls(get_model_id(child), get_model_id(parent), tags=("subclass",))

    @classmethod
    def from_field(
        cls, model: type[models.Model], field: type[models.fields.Field]
    ) -> Edge | None:
        # Ignore non-relation fields
        if not field.is_relation:
            return None
        # Skip fields defined on superclasses
        if field.model != model:
            return None
        related_model = field.related_model
        # GenericForeignKey
        if related_model is None:
            return None
        model_id = get_model_id(model)
        related_model_id = get_model_id(related_model)
        # Foreign key
        if field.many_to_one:
            return cls(model_id, related_model_id, tags=("foreign-key",))
        # One to one
        elif field.one_to_one and not field.auto_created:
            return cls(model_id, related_model_id, tags=("one-to-one",))
        # Many-to-many
        elif field.many_to_many and not field.auto_created:
            through_model = getattr(model, field.name).through
            # We only add the M2M connection if the through-model is auto-created.
            # This stops us from creating two sets of connections (because the
            # connections will be created by the FK fields on the through model).
            if through_model._meta.auto_created:
                return cls(model_id, related_model_id, tags=("many-to-many",))


@attrs.frozen(order=True)
class Group:
    id: str
    name: str

    @classmethod
    def from_model(cls, model: type[models.Model]) -> Group:
        return cls(id=get_app_name(model), name=get_app_name(model))


@attrs.frozen
class Graph:
    nodes: tuple[Node, ...]
    edges: tuple[Edge, ...]
    groups: tuple[Group, ...]


def get_app_models() -> Iterator[tuple[apps.AppConfig, type[models.Model]]]:
    for app in apps.apps.get_app_configs():
        for model in app.get_models():
            yield app, model


def get_app_name(model: type[models.Model]) -> str:
    app_label = model._meta.app_label
    try:
        return apps.apps.get_app_config(app_label).name
    except LookupError:
        return model.__module__


def get_model_id(model: type[models.Model]) -> str:
    return f"{model.__module__}.{model.__name__}"


def is_model_subclass(obj):
    if obj is models.Model:
        return False
    return issubclass(obj, models.Model)


def get_schema() -> Graph:
    nodes = set()
    edges = set()
    groups = set()

    for app, model in get_app_models():
        nodes.add(Node.from_model(model))
        groups.add(Group.from_model(model))

        # Proxy models
        if model._meta.proxy:
            edges.add(Edge.proxy(model, model._meta.proxy_for_model))
            continue

        # Subclassing
        for base in filter(is_model_subclass, model.__mro__):
            nodes.add(Node.from_model(base))
            groups.add(Group.from_model(base))
            for parent in filter(is_model_subclass, base.__bases__):
                edges.add(Edge.subclass(base, parent))

        # Relationships
        for field in model._meta.get_fields():
            edge = Edge.from_field(model, field)
            if edge is None:
                continue
            edges.add(edge)

    return Graph(
        nodes=tuple(sorted(nodes)),
        edges=tuple(sorted(edges)),
        groups=tuple(sorted(groups)),
    )
