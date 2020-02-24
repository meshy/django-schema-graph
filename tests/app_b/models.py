from django.db import models


class InterAppForeignKey(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
