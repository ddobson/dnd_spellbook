from rest_framework import serializers
from dnd_spellbook import constants as const


def validate_contains_id(value):
    for spell in value:
        if not spell.get("id", None):
            raise serializers.ValidationError(const.SPELL_DOES_NOT_CONTAIN_ID)


def validate_classes(values):
    for character_class in values:
        if character_class not in const.VALID_CHARACTER_CLASSES:
            raise serializers.ValidationError(const.CLASSES_VALIDATION_ERROR)


def validate_spell_classes(func):
    def any_in(a, b):
        return any(i in b for i in a)

    def wrapper(spellbook, spells, *args, **kwargs):
        spellbook.refresh_from_db()
        instance_spells = spellbook.spells.all()
        invalid_spells = []

        for spell in spells:
            if not any_in(spell.classes, spellbook.classes):
                invalid_spells.append(spell)

        if invalid_spells:
            raise serializers.ValidationError(
                {"spells": [const.SPELLBOOK_SPELL_CLASS_VALIDATION_ERROR]}
            )

        return func(spellbook, spells, *args, **kwargs)

    return wrapper
