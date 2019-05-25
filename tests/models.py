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
