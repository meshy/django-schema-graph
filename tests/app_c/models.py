from django.db import models


class InterAppOneToOne(models.Model):
    user = models.OneToOneField("app_b.InterAppForeignKey", on_delete=models.CASCADE)
