from rest_framework.serializers import ModelSerializer
from spells.models import Spell


class SpellSerializer(ModelSerializer):
    class Meta:
        model = Spell
        fields = (
            'id',
            'casting_time',
            'classes',
            'components',
            'description',
            'higher_levels',
            'duration',
            'level',
            'name',
            'spell_range',
            'ritual',
            'school',
            'spell_type',
        )
