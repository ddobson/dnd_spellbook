from rest_framework.serializers import (CurrentUserDefault, HiddenField, ModelSerializer)
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
    user = HiddenField(default=CurrentUserDefault())

    def __init__(self, *args, **kwargs):
        super(SpellbookSerializer, self).__init__(*args, **kwargs)

        request = kwargs['context']['request']
        include_spells = request.GET.get('include_spells', False)

        if include_spells:
            self.fields['spells'] = SpellSerializer(
                many=True, context=kwargs['context'])

    class Meta:
        model = Spellbook
        fields = (
            'id',
            'name',
            'description',
            'classes',
            'user',
        )
