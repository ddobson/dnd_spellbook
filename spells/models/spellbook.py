from django.db.models.signals import m2m_changed
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

from spells.models.spell import Spell
from spells.validators import validate_spell_classes

DEFAULT_USER_ID = 1


class Spellbook(models.Model):
    class Meta:
        ordering = ['id']

    name = models.CharField(blank=False, null=False, default="Generic Spellbook", max_length=64)
    description = models.CharField(blank=True, null=True, max_length=256)
    classes = ArrayField(models.CharField(max_length=24, blank=True), default=list, size=24)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, default=DEFAULT_USER_ID)
    spells = models.ManyToManyField(
        Spell,
        related_name="spellbooks",
    )


m2m_changed.connect(validate_spell_classes, sender=Spellbook.spells.through)
