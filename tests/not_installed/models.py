from django.db import models


class AbstractNotInstalled(models.Model):
    class Meta:
        abstract = True
