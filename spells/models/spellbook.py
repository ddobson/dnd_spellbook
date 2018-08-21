from django.db import models
from django.contrib.postgres.fields import ArrayField
from dnd_spellbook import constants as const
from spells.models.spell import Spell


class Spellbook(models.Model):
    class Meta:
        ordering = ["id"]

    name = models.CharField(
        blank=False, null=False, default="Generic Spellbook", max_length=64
    )
    description = models.CharField(blank=True, null=True, max_length=256)
    classes = ArrayField(
        models.CharField(max_length=24, blank=True), default=list, size=24
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, default=const.DEFAULT_USER_ID
    )
    spells = models.ManyToManyField(Spell, related_name="spellbooks")
