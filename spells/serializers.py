from django.db import transaction
from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    HiddenField,
    ListField,
    ModelSerializer
)
from spells.validators import validate_classes
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
    classes = ListField(
        child=CharField(),
        validators=[validate_classes]
    )

    class Meta:
        model = Spellbook
        fields = (
            'id',
            'name',
            'description',
            'classes',
            'user',
        )

    def __init__(self, *args, **kwargs):
        super(SpellbookSerializer, self).__init__(*args, **kwargs)

        request = kwargs['context']['request']
        include_spells = request.GET.get('include_spells', False)

        if include_spells:
            self.fields['spells'] = SpellSerializer(
                many=True, context=kwargs['context'])

    def find_spells(self, spell_ids):
        spells = set()
        for spell in spell_ids:
            spells.add(Spell.objects.get(pk=spell['id']))
        return spells

    def process_spellbook_spell_updates(self, spellbook, request_spells_set, instance_spells_set):
        spellbook.spells.add(*request_spells_set.difference(instance_spells_set))
        spellbook.spells.remove(*instance_spells_set.difference(request_spells_set))

    @transaction.atomic
    def create(self, validated_data):
        spellbook = Spellbook.objects.create(**validated_data)
        if 'spells' in self.initial_data:
            spells = self.find_spells(self.initial_data.get('spells'))
            spellbook.spells.add(*spells)
        return spellbook

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'spells' in self.initial_data:
            request_spells_set = self.find_spells(self.initial_data.get('spells'))
            instance_spells_set = set(instance.spells.all())
            self.process_spellbook_spell_updates(instance, request_spells_set, instance_spells_set)
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance
