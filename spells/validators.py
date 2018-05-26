from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dnd_spellbook.utils import constants
from spells.models.spell import Spell


def validate_classes(values):
    for character_class in values:
        if character_class not in constants.VALID_CHARACTER_CLASSES:
            raise serializers.ValidationError(constants.CLASSES_VALIDATION_ERROR)


def validate_spell_classes(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action != 'pre_add':
        return

    def any_in(a, b):
        return any(i in b for i in a)

    spells = Spell.objects.filter(pk__in=pk_set)
    invalid_spells = []

    for spell in spells:
        if not any_in(spell.classes, instance.classes):
            invalid_spells.append(spell)

    if invalid_spells:
        raise serializers.ValidationError(
            _("One or more of the spells you tried to add are not of valid character classes for this spellbook")  # noqa
        )
