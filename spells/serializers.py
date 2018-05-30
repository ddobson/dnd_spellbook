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

    def validate_spell_classes(self, spellbook, spells):
        validators.validate_spell_classes(spellbook, spells)
        return spellbook

    def find_spells(self, spell_ids):
        spells = set()
        for spell in spell_ids:
            spells.add(Spell.objects.get(pk=spell['id']))
        return spells

    def process_spellbook_spell_updates(self, spellbook, request_spells_set, instance_spells_set):
        self.validate_spell_classes(spellbook, request_spells_set)
        spellbook.spells.add(*request_spells_set.difference(instance_spells_set))
        spellbook.spells.remove(*instance_spells_set.difference(request_spells_set))

    @transaction.atomic
    def create(self, validated_data):
        validated_spells = validated_data.pop('spells')
        spellbook = Spellbook.objects.create(**validated_data)
        if validated_spells:
            spells = self.find_spells(validated_spells)
            self.validate_spell_classes(spellbook, spells)
            spellbook.spells.add(*spells)
        return spellbook

    @transaction.atomic
    def update(self, instance, validated_data):
        # Remove any spells that are no longer vaild when an update triggers a class change
        if validated_data.get('classes'):
            spells_to_remove = instance.spells.exclude(classes__contains=validated_data.get('classes'))
            if spells_to_remove.exists():
                instance.spells.remove(*spells_to_remove)

        # Handle updates to the spellbooks spell list w/ validation
        if validated_data.get('spells'):
            validated_spells = validated_data.pop('spells')
            Spellbook.objects.filter(pk=instance.pk).update(**validated_data)
            request_spells_set = self.find_spells(validated_spells)
            instance_spells_set = set(instance.spells.all())
            self.process_spellbook_spell_updates(instance, request_spells_set, instance_spells_set)
        else:
            Spellbook.objects.filter(pk=instance.pk).update(**validated_data)
            instance.refresh_from_db()

        return instance
