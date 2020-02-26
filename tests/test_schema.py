import django

from schema_graph.schema import get_schema


DJANGO_LT_19 = django.VERSION < (1, 9, 0)


def test_abstract_models():
    expected = {
        "django.contrib.auth": ("AbstractBaseUser", "AbstractUser", "PermissionsMixin"),
        "django.contrib.sessions": ("AbstractBaseSession",),
        "tests.inheritance": (
            "Abstract",
            "AbstractBase",
            "AbstractSubclass1",
            "AbstractSubclass2",
        ),
    }
    if DJANGO_LT_19:
        expected.pop("django.contrib.sessions")
    assert get_schema().abstract_models == expected


def test_models():
    expected = {
        "django.contrib.auth": ("Group", "Permission", "User"),
        "django.contrib.contenttypes": ("ContentType",),
        "django.contrib.sessions": ("Session",),
        "django.contrib.sites": ("Site",),
        "tests": (
            "AnotherOneToOne",
            "GenericFK",
            "NoOutgoingConnections",
            "OutgoingForeignKey",
            "OutgoingManyToMany",
            "OutgoingOneToOne",
            "ProxyNode",
            "ProxyNode2",
            "SelfReference",
        ),
        "tests.inheritance": (
            "AbstractMultipleInheritance",
            "Concrete",
            "ConcreteBase",
            "ConcreteInheritance",
            "ConcreteSubclass1",
            "ConcreteSubclass2",
            "MixedMultipleInheritance",
            "SubSubclass",
            "Subclass",
        ),
    }
    assert get_schema().models == expected


def test_foreign_key():
    expected = [
        (
            ("django.contrib.auth", "Permission"),
            ("django.contrib.contenttypes", "ContentType"),
        ),
        (("tests", "GenericFK"), ("django.contrib.contenttypes", "ContentType")),
        (("tests", "OutgoingForeignKey"), ("tests", "NoOutgoingConnections")),
        (("tests", "SelfReference"), ("tests", "SelfReference")),
    ]
    assert get_schema().foreign_keys == expected


def test_one_to_one():
    expected = [
        (("tests", "AnotherOneToOne"), ("tests", "NoOutgoingConnections")),
        (("tests", "OutgoingOneToOne"), ("tests", "NoOutgoingConnections")),
        (
            ("tests.inheritance", "ConcreteSubclass2"),
            ("tests.inheritance", "ConcreteBase"),
        ),
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
        (
            ("django.contrib.auth", "AbstractUser"),
            ("django.contrib.auth", "AbstractBaseUser"),
        ),
        (
            ("django.contrib.auth", "AbstractUser"),
            ("django.contrib.auth", "PermissionsMixin"),
        ),
        (("django.contrib.auth", "User"), ("django.contrib.auth", "AbstractUser")),
        (
            ("django.contrib.sessions", "Session"),
            ("django.contrib.sessions", "AbstractBaseSession"),
        ),
        (
            ("tests.inheritance", "AbstractMultipleInheritance"),
            ("tests.inheritance", "AbstractSubclass1"),
        ),
        (
            ("tests.inheritance", "AbstractMultipleInheritance"),
            ("tests.inheritance", "AbstractSubclass2"),
        ),
        (
            ("tests.inheritance", "AbstractSubclass1"),
            ("tests.inheritance", "AbstractBase"),
        ),
        (
            ("tests.inheritance", "AbstractSubclass2"),
            ("tests.inheritance", "AbstractBase"),
        ),
        (("tests.inheritance", "Concrete"), ("tests.inheritance", "Abstract")),
        (
            ("tests.inheritance", "ConcreteInheritance"),
            ("tests.inheritance", "ConcreteSubclass1"),
        ),
        (
            ("tests.inheritance", "ConcreteInheritance"),
            ("tests.inheritance", "ConcreteSubclass2"),
        ),
        (
            ("tests.inheritance", "ConcreteSubclass1"),
            ("tests.inheritance", "ConcreteBase"),
        ),
        (
            ("tests.inheritance", "ConcreteSubclass2"),
            ("tests.inheritance", "ConcreteBase"),
        ),
        (
            ("tests.inheritance", "MixedMultipleInheritance"),
            ("tests.inheritance", "AbstractBase"),
        ),
        (
            ("tests.inheritance", "MixedMultipleInheritance"),
            ("tests.inheritance", "ConcreteBase"),
        ),
        (("tests.inheritance", "SubSubclass"), ("tests.inheritance", "Subclass")),
        (("tests.inheritance", "Subclass"), ("tests.inheritance", "ConcreteBase")),
    ]
    if DJANGO_LT_19:
        expected.remove(
            (
                ("django.contrib.sessions", "Session"),
                ("django.contrib.sessions", "AbstractBaseSession"),
            )
        )
    assert get_schema().inheritance == expected


def test_proxy():
    expected = [
        (("tests", "ProxyNode"), ("tests", "OutgoingManyToMany")),
        (("tests", "ProxyNode2"), ("tests", "OutgoingOneToOne")),
    ]
    assert get_schema().proxies == expected
