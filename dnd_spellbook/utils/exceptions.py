from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from spells.models.spell import Spell
from spells.views import SpellbookView
from . import constants as const


def dnd_spellbook_app_exception_handler(exc, context):
    if isinstance(exc, Spell.DoesNotExist) and isinstance(context['view'], SpellbookView):
        return Response(
            data={'spells': [const.SPELLBOOK_SPELL_NOT_FOUND_ERROR]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return exception_handler(exc, context)
