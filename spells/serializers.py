from django.db import transaction
from rest_framework.serializers import CurrentUserDefault, HiddenField, ModelSerializer
from spells.models.spell import Spell
from spells.models.spellbook import Spellbook


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

    @transaction.atomic
    def create(self, validated_data):
        spellbook = Spellbook.objects.create(**validated_data)
        if 'spells' in self.initial_data:
            spell_ids = self.initial_data.get('spells')
            spells = Spell.objects.filter(pk__in=[spell['id'] for spell in spell_ids])
            spellbook.spells.add(*spells)
        return spellbook

    class Meta:
        model = Spellbook
        fields = (
            'id',
            'name',
            'description',
            'classes',
            'user',
        )
