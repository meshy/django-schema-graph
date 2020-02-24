from django.db import models

from ..app_c.models import InterAppOneToOne


class InterAppManyToMany(models.Model):
    user = models.ManyToManyField("app_b.InterAppForeignKey")


class InterAppProxy(InterAppOneToOne):
    class Meta:
        proxy = True
