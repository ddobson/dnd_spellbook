from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class Spell(models.Model):
    class Meta:
        ordering = ['id']

    casting_time = models.CharField(blank=True, null=True, max_length=128)
    classes = ArrayField(
        models.CharField(max_length=24, blank=True),
        size=24,
    )
    components = JSONField()
    description = models.CharField(blank=True, null=True, max_length=10240)
    higher_levels = models.CharField(blank=True, null=True, max_length=1024)
    duration = models.CharField(blank=True, null=True, max_length=128)
    level = models.SmallIntegerField(default=0)
    name = models.CharField(blank=True, null=True, max_length=128)
    spell_range = models.CharField(blank=True, null=True, max_length=128)
    ritual = models.BooleanField(default=False)
    school = models.CharField(blank=True, null=True, max_length=128)
    spell_type = models.CharField(blank=True, null=True, max_length=128)
