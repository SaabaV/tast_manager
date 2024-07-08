from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=70, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'

