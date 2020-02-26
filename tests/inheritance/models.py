from django.db import models


class ConcreteBase(models.Model):
    pass


class Subclass(ConcreteBase):
    pass


class SubSubclass(Subclass):
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


class Abstract(models.Model):
    class Meta:
        abstract = True


class Concrete(Abstract):
    pass
