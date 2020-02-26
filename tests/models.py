from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models


class NoOutgoingConnections(models.Model):
    pass


class OutgoingManyToMany(models.Model):
    connected = models.ManyToManyField("NoOutgoingConnections")


class OutgoingForeignKey(models.Model):
    connected = models.ForeignKey("NoOutgoingConnections", on_delete=models.CASCADE)


class OutgoingOneToOne(models.Model):
    connected = models.OneToOneField("NoOutgoingConnections", on_delete=models.CASCADE)


class AnotherOneToOne(models.Model):
    connected = models.OneToOneField("NoOutgoingConnections", on_delete=models.CASCADE)


class SelfReference(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE)


class Subclass(NoOutgoingConnections):
    pass


class SubSubclass(Subclass):
    pass


class ConcreteBase(models.Model):
    pass


class ConcreteSubclass1(ConcreteBase):
    pass


class ConcreteSubclass2(ConcreteBase):
    # Required to avoid clash with ConcreteSubclass2.concretebase_ptr
    parent_ptr = models.OneToOneField(
        ConcreteBase, on_delete=models.CASCADE, parent_link=True
    )


class ConcreteInheritance(ConcreteSubclass1, ConcreteSubclass2):
    pass


class AbstractBase(models.Model):
    class Meta:
        abstract = True


class AbstractSubclass1(AbstractBase):
    class Meta:
        abstract = True


class AbstractSubclass2(AbstractBase):
    class Meta:
        abstract = True


class AbstractMultipleInheritance(AbstractSubclass1, AbstractSubclass2):
    pass


class MixedMultipleInheritance(AbstractBase, ConcreteBase):
    pass


class Subclass2(OutgoingForeignKey):
    pass


class Abstract(models.Model):
    connected = models.ForeignKey("NoOutgoingConnections", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Concrete(Abstract):
    pass


class ProxyNode2(OutgoingOneToOne):
    class Meta:
        proxy = True


class ProxyNode(OutgoingManyToMany):
    class Meta:
        proxy = True


class GenericFK(models.Model):
    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
