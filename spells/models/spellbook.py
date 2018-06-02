from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from dnd_spellbook.utils import constants as const
from spells import validators
from spells.models.spell import Spell
from spells.validators import validate_spell_classes


class Spellbook(models.Model):
    class Meta:
        ordering = ['id']

    name = models.CharField(blank=False, null=False,
                            default="Generic Spellbook", max_length=64)
    description = models.CharField(blank=True, null=True, max_length=256)
    classes = ArrayField(models.CharField(
        max_length=24, blank=True), default=list, size=24)
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, default=const.DEFAULT_USER_ID)
    spells = models.ManyToManyField(
        Spell,
        related_name="spellbooks",
    )

    @validators.validate_spell_classes
    def process_spellbook_spell_additions(self, spells):
        self.spells.add(*spells)
        return self

    def process_spellbook_spell_removals(self, spells):
        self.spells.remove(*spells)
        return self

    def update_spellbook_spells_by_difference(self, request_spells, current_spells):
        spell_additions = request_spells.difference(current_spells)
        spell_removals = current_spells.difference(request_spells)
        self.process_spellbook_spell_additions(spell_additions)
        self.process_spellbook_spell_removals(spell_removals)
        return self

    def remove_existing_spells_on_class_list_update(self, classes_list):
        spells_to_remove = self.spells.exclude(classes__contains=classes_list)
        self.process_spellbook_spell_removals(spells_to_remove)
        return self
