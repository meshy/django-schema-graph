from django.db import models


class Target(models.Model):
    pass


class ProxyNode2(Target):
    class Meta:
        proxy = True


class ProxyNode(Target):
    class Meta:
        proxy = True
