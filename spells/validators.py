from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from spells.models.spell import Spell


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
        raise ValidationError(
            _("One or more of the spells you tried to add are not of valid character classes for this spellbook")  # noqa
        )
