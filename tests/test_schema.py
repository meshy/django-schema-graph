from schema_graph.schema import get_schema


def test_models():
    expected = {
        "django.contrib.auth": ("Group", "Permission", "User"),
        "django.contrib.contenttypes": ("ContentType",),
        "django.contrib.sessions": ("Session",),
        "django.contrib.sites": ("Site",),
        "tests": (
            "AnotherOneToOne",
            "Concrete",
            "GenericFK",
            "NoOutgoingConnections",
            "OutgoingForeignKey",
            "OutgoingManyToMany",
            "OutgoingOneToOne",
            "ProxyNode",
            "ProxyNode2",
            "SelfReference",
            "SubSubclass",
            "Subclass",
            "Subclass2",
        ),
    }
    assert get_schema().models == expected


def test_foreign_key():
    expected = [
        (
            ("django.contrib.auth", "Permission"),
            ("django.contrib.contenttypes", "ContentType"),
        ),
        (("tests", "Concrete"), ("tests", "NoOutgoingConnections")),
        (("tests", "GenericFK"), ("django.contrib.contenttypes", "ContentType")),
        (("tests", "OutgoingForeignKey"), ("tests", "NoOutgoingConnections")),
        (("tests", "SelfReference"), ("tests", "SelfReference")),
    ]
    assert get_schema().foreign_keys == expected


def test_one_to_one():
    expected = [
        (("tests", "AnotherOneToOne"), ("tests", "NoOutgoingConnections")),
        (("tests", "OutgoingOneToOne"), ("tests", "NoOutgoingConnections")),
    ]
    assert get_schema().one_to_ones == expected


def test_many_to_many():
    expected = [
        (("django.contrib.auth", "Group"), ("django.contrib.auth", "Permission")),
        (("django.contrib.auth", "User"), ("django.contrib.auth", "Group")),
        (("django.contrib.auth", "User"), ("django.contrib.auth", "Permission")),
        (("tests", "OutgoingManyToMany"), ("tests", "NoOutgoingConnections")),
    ]
    assert get_schema().many_to_manys == expected


def test_inheritance():
    expected = [
        (("tests", "SubSubclass"), ("tests", "Subclass")),
        (("tests", "Subclass"), ("tests", "NoOutgoingConnections")),
        (("tests", "Subclass2"), ("tests", "OutgoingForeignKey")),
    ]
    assert get_schema().inheritance == expected


def test_proxy():
    expected = [
        (("tests", "ProxyNode"), ("tests", "OutgoingManyToMany")),
        (("tests", "ProxyNode2"), ("tests", "OutgoingOneToOne")),
    ]
    assert get_schema().proxies == expected
