from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from dnd_spellbook.utils import constants as const
from spells import validators
from spells.models.spell import Spell
from spells.validators import validate_spell_classes


class Spellbook(models.Model):
    class Meta:
        ordering = ['id']

    name = models.CharField(blank=False, null=False, default="Generic Spellbook", max_length=64)
    description = models.CharField(blank=True, null=True, max_length=256)
    classes = ArrayField(models.CharField(max_length=24, blank=True), default=list, size=24)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, default=const.DEFAULT_USER_ID)
    spells = models.ManyToManyField(
        Spell,
        related_name="spellbooks",
    )

    def process_spellbook_spell_updates(self, request_spells_set):
        current_spell_set = set(self.spells.all())
        validate_spell_classes(self, request_spells_set)
        self.spells.add(*request_spells_set.difference(current_spell_set))
        self.spells.remove(*current_spell_set.difference(request_spells_set))
        return self

    def remove_existing_spells_on_class_list_update(self, classes_list):
        spells_to_remove = self.spells.exclude(classes__contains=classes_list)
        self.spells.remove(*spells_to_remove)
        return self
