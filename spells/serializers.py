from rest_framework.serializers import ModelSerializer
from spells.models import (Spellbook, Spell)


class SpellSerializer(ModelSerializer):
    class Meta:
        model = Spell
        fields = (
            'id',
            'name',
            'classes',
            'level',
            'school',
            'duration',
            'casting_time',
            'components',
            'spell_range',
            'ritual',
            'description',
            'higher_levels',
            'spell_type',
        )


class SpellbookSerializer(ModelSerializer):
    spells = SpellSerializer(many=True, read_only=True)

    class Meta:
        model = Spellbook
        fields = (
            'id',
            'name',
            'description',
            'classes',
            'user',
            'spells',
        )
