from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from spells.models.spell import Spell
from spells.views import SpellbookView

SPELLBOOK_SPELL_NOT_FOUND_ERROR = "One or more of the spells you tried to add could not be found."
SPELLBOOK_SPELL_CLASS_VALIDATION_ERROR = "One or more of the spells you tried to add are not of valid character classes for this spellbook"  # noqa


def dnd_spellbook_app_exception_handler(exc, context):
    if isinstance(exc, Spell.DoesNotExist) and isinstance(context['view'], SpellbookView):
        return Response(
            data={'detail': SPELLBOOK_SPELL_NOT_FOUND_ERROR},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif isinstance(exc, ValidationError) and exc.message == SPELLBOOK_SPELL_CLASS_VALIDATION_ERROR:
        return Response(
            data={'detail': SPELLBOOK_SPELL_CLASS_VALIDATION_ERROR},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        return exception_handler(exc, context)
