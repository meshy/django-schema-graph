from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models


class GenericFK(models.Model):
    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
