from schema_graph.schema import get_schema

from django.test import TestCase


class TestGetSchema(TestCase):
    @classmethod
    def setUpTestData(self):
        (
            self.nodes,
            self.fk,
            self.o2o,
            self.m2m,
            self.implicit_fk,
            self.implicit_o2o,
            self.implicit_m2m,
            self.is_a,
        ) = get_schema()

    def test_nodes(self):
        expected = [
            ('django.contrib.auth', 'Group'),
            ('django.contrib.auth', 'Permission'),
            ('django.contrib.auth', 'User'),
            ('django.contrib.contenttypes', 'ContentType'),
            ('django.contrib.sessions', 'Session'),
            ('django.contrib.sites', 'Site'),
            ('schema_graph.tests', 'NoOutgoingConnections'),
            ('schema_graph.tests', 'OutgoingForeignKey'),
            ('schema_graph.tests', 'OutgoingManyToMany'),
            ('schema_graph.tests', 'OutgoingOneToOne'),
            ('schema_graph.tests', 'SelfReference'),
        ]
        self.assertEqual(self.nodes, expected)

    def test_foreign_key(self):
        self.fail()

    def test_one_to_one(self):
        self.fail()

    def test_many_to_many(self):
        self.fail()

    def test_implicit_foreign_key(self):
        self.fail()

    def test_implicit_one_to_one(self):
        self.fail()

    def test_implicit_many_to_many(self):
        self.fail()
