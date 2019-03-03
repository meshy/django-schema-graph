from schema_graph.schema import get_schema

from django.test import TestCase


class TestGetSchema(TestCase):
    def setUp(self):
        self.nodes, self.edges = get_schema()

    def test_nodes(self):
        self.fail()

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
