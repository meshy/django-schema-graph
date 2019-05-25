from django.test import TestCase

from schema_graph.schema import get_schema


class TestGetSchema(TestCase):
    @classmethod
    def setUpTestData(self):
        schema = get_schema()
        # Vertices
        self.nodes = schema.models
        self.proxy = schema.proxies
        # Edges
        self.fk = schema.foreign_keys
        self.o2o = schema.one_to_ones
        self.m2m = schema.many_to_manys
        self.is_a = schema.inheritance

    def test_nodes(self):
        expected = [
            ("django.contrib.auth", "Group"),
            ("django.contrib.auth", "Permission"),
            ("django.contrib.auth", "User"),
            ("django.contrib.contenttypes", "ContentType"),
            ("django.contrib.sessions", "Session"),
            ("django.contrib.sites", "Site"),
            ("tests", "AnotherOneToOne"),
            ("tests", "Concrete"),
            ("tests", "NoOutgoingConnections"),
            ("tests", "OutgoingForeignKey"),
            ("tests", "OutgoingManyToMany"),
            ("tests", "OutgoingOneToOne"),
            ("tests", "ProxyNode"),
            ("tests", "ProxyNode2"),
            ("tests", "SelfReference"),
            ("tests", "SubSubclass"),
            ("tests", "Subclass"),
            ("tests", "Subclass2"),
        ]
        assert self.nodes == expected

    def test_foreign_key(self):
        expected = [
            (
                ("django.contrib.auth", "Permission"),
                ("django.contrib.contenttypes", "ContentType"),
            ),
            (("tests", "Concrete"), ("tests", "NoOutgoingConnections")),
            (("tests", "OutgoingForeignKey"), ("tests", "NoOutgoingConnections")),
            (("tests", "SelfReference"), ("tests", "SelfReference")),
        ]
        assert self.fk == expected

    def test_one_to_one(self):
        expected = [
            (("tests", "AnotherOneToOne"), ("tests", "NoOutgoingConnections")),
            (("tests", "OutgoingOneToOne"), ("tests", "NoOutgoingConnections")),
        ]
        assert self.o2o == expected

    def test_many_to_many(self):
        expected = [
            (("django.contrib.auth", "Group"), ("django.contrib.auth", "Permission")),
            (("django.contrib.auth", "User"), ("django.contrib.auth", "Group")),
            (("django.contrib.auth", "User"), ("django.contrib.auth", "Permission")),
            (("tests", "OutgoingManyToMany"), ("tests", "NoOutgoingConnections")),
        ]
        assert self.m2m == expected

    def test_inheritance(self):
        expected = [
            (("tests", "SubSubclass"), ("tests", "Subclass")),
            (("tests", "Subclass"), ("tests", "NoOutgoingConnections")),
            (("tests", "Subclass2"), ("tests", "OutgoingForeignKey")),
        ]
        assert self.is_a == expected

    def test_proxy(self):
        expected = [
            (("tests", "ProxyNode"), ("tests", "OutgoingManyToMany")),
            (("tests", "ProxyNode2"), ("tests", "OutgoingOneToOne")),
        ]
        assert self.proxy == expected
