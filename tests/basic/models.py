from django.db import models


class SelfReference(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE)


class Target(models.Model):
    pass


class OutgoingManyToMany(models.Model):
    connected = models.ManyToManyField(Target)


class OutgoingForeignKey(models.Model):
    connected = models.ForeignKey(Target, on_delete=models.CASCADE)


class OutgoingOneToOne(models.Model):
    connected = models.OneToOneField(Target, on_delete=models.CASCADE)


class ThroughTable(models.Model):
    source = models.ForeignKey("ManyToManyWithThroughTable", on_delete=models.CASCADE)
    target = models.ForeignKey(Target, on_delete=models.CASCADE)


class ManyToManyWithThroughTable(models.Model):
    connected = models.ManyToManyField(Target, through=ThroughTable)
