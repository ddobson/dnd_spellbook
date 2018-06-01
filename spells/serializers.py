from django.db import transaction
from rest_framework import serializers
from dnd_spellbook.utils import constants
from spells import validators
from spells.models.spell import Spell
from spells.models.spellbook import Spellbook


class SpellSerializer(serializers.ModelSerializer):
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

    def to_internal_value(self, data):
        """
        Dict of native values <- Dict of primitive datatypes.
        Add instance key to values if `id` present in primitive dict
        :param data:
        """
        obj = super(SpellSerializer, self).to_internal_value(data)
        for key in data.keys():
            obj[key] = data[key]
        return obj


class SpellbookSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    classes = serializers.ListField(
        child=serializers.CharField(),
    )
    spells = SpellSerializer(
        many=True,
        read_only=False,
    )

    class Meta:
        model = Spellbook
        fields = (
            'id',
            'name',
            'description',
            'classes',
            'spells',
            'user',
        )

    def __init__(self, *args, **kwargs):
        super(SpellbookSerializer, self).__init__(*args, **kwargs)

        request = kwargs['context']['request']
        hide_spells = request.GET.get('hide_spells', False)

        if hide_spells:
            self.fields.pop('spells')

    def validate_classes(self, value):
        validators.validate_classes(value)
        return value

    def validate_spells(self, value):
        validators.validate_contains_id(value)
        return value

    def find_spells_from_validated_data(self, spell_ids):
        spells = set()
        for spell in spell_ids:
            spells.add(Spell.objects.get(pk=spell['id']))
        return spells

    @transaction.atomic
    def create(self, validated_data):
        validated_spells = validated_data.pop('spells')
        spellbook = Spellbook.objects.create(**validated_data)
        if validated_spells:
            spells = self.find_spells_from_validated_data(validated_spells)
            spellbook.process_spellbook_spell_updates(spells)
        return spellbook

    @transaction.atomic
    def update(self, spellbook, validated_data):
        # Remove any spells that are no longer valid when an update triggers a class change
        if validated_data.get('classes'):
            spellbook.remove_existing_spells_on_class_list_update(validated_data.get('classes'))

        # Handle updates to the spellbooks spell list w/ validation
        if validated_data.get('spells'):
            validated_spells = validated_data.pop('spells')
            Spellbook.objects.filter(pk=spellbook.pk).update(**validated_data)
            request_spells_set = self.find_spells_from_validated_data(validated_spells)
            instance_spells_set = set(spellbook.spells.all())
            spellbook.process_spellbook_spell_updates(request_spells_set)
        else:
            Spellbook.objects.filter(pk=spellbook.pk).update(**validated_data)
            spellbook.refresh_from_db()

        return spellbook
