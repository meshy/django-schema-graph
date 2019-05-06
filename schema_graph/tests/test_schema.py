from django.test import TestCase

from schema_graph.schema import get_schema


class TestGetSchema(TestCase):
    @classmethod
    def setUpTestData(self):
        (self.nodes, self.fk, self.o2o, self.m2m, self.is_a, self.proxy) = get_schema()

    def test_nodes(self):
        expected = [
            ("django.contrib.auth", "Group"),
            ("django.contrib.auth", "Permission"),
            ("django.contrib.auth", "User"),
            ("django.contrib.contenttypes", "ContentType"),
            ("django.contrib.sessions", "Session"),
            ("django.contrib.sites", "Site"),
            ("schema_graph.tests", "AnotherOneToOne"),
            ("schema_graph.tests", "NoOutgoingConnections"),
            ("schema_graph.tests", "OutgoingForeignKey"),
            ("schema_graph.tests", "OutgoingManyToMany"),
            ("schema_graph.tests", "OutgoingOneToOne"),
            ("schema_graph.tests", "ProxyNode"),
            ("schema_graph.tests", "ProxyNode2"),
            ("schema_graph.tests", "SelfReference"),
            ("schema_graph.tests", "SubSubclass"),
            ("schema_graph.tests", "Subclass"),
            ("schema_graph.tests", "Subclass2"),
        ]
        self.assertEqual(self.nodes, expected)

    def test_foreign_key(self):
        expected = [
            (
                ("django.contrib.auth", "Permission"),
                ("django.contrib.contenttypes", "ContentType"),
            ),
            (
                ("schema_graph.tests", "OutgoingForeignKey"),
                ("schema_graph.tests", "NoOutgoingConnections"),
            ),
            (
                ("schema_graph.tests", "SelfReference"),
                ("schema_graph.tests", "SelfReference"),
            ),
        ]
        self.assertEqual(self.fk, expected)

    def test_one_to_one(self):
        expected = [
            (
                ("schema_graph.tests", "AnotherOneToOne"),
                ("schema_graph.tests", "NoOutgoingConnections"),
            ),
            (
                ("schema_graph.tests", "OutgoingOneToOne"),
                ("schema_graph.tests", "NoOutgoingConnections"),
            ),
        ]
        self.assertEqual(self.o2o, expected)

    def test_many_to_many(self):
        expected = [
            (("django.contrib.auth", "Group"), ("django.contrib.auth", "Permission")),
            (("django.contrib.auth", "User"), ("django.contrib.auth", "Group")),
            (("django.contrib.auth", "User"), ("django.contrib.auth", "Permission")),
            (
                ("schema_graph.tests", "OutgoingManyToMany"),
                ("schema_graph.tests", "NoOutgoingConnections"),
            ),
        ]
        self.assertEqual(self.m2m, expected)

    def test_inheritance(self):
        expected = [
            (("schema_graph.tests", "SubSubclass"), ("schema_graph.tests", "Subclass")),
            (
                ("schema_graph.tests", "Subclass"),
                ("schema_graph.tests", "NoOutgoingConnections"),
            ),
            (
                ("schema_graph.tests", "Subclass2"),
                ("schema_graph.tests", "OutgoingForeignKey"),
            ),
        ]
        assert self.is_a == expected

    def test_proxy(self):
        expected = [
            (
                ("schema_graph.tests", "ProxyNode"),
                ("schema_graph.tests", "OutgoingManyToMany"),
            ),
            (
                ("schema_graph.tests", "ProxyNode2"),
                ("schema_graph.tests", "OutgoingOneToOne"),
            ),
        ]
        self.assertEqual(self.proxy, expected)
