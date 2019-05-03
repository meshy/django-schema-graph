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
