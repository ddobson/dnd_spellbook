import itertools
from django.db import transaction
from rest_framework import serializers
from dnd_spellbook import constants
from .models import Spell
from .models import Spellbook
from .services.spellbook_service import SpellbookService


class SpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spell
        fields = (
            "id",
            "name",
            "classes",
            "level",
            "school",
            "duration",
            "casting_time",
            "components",
            "spell_range",
            "ritual",
            "description",
            "higher_levels",
            "spell_type",
        )

    id = serializers.ModelField(required=False, model_field=Spell()._meta.get_field("id"))


class SpellbookSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    classes = serializers.ListField(child=serializers.CharField())
    spells = SpellSerializer(many=True, read_only=False)

    class Meta:
        model = Spellbook
        fields = ("id", "name", "description", "classes", "spells", "user")

    def __init__(self, *args, **kwargs):
        super(SpellbookSerializer, self).__init__(*args, **kwargs)

        request = kwargs["context"]["request"]
        hide_spells = request.GET.get("hide_spells", False)

        if hide_spells:
            self.fields.pop("spells")

    def validate_classes(self, value):
        for character_class in value:
            if character_class not in Spell.distinct_classes():
                raise serializers.ValidationError(
                    constants.CLASSES_VALIDATION_ERROR.format(Spell.distinct_classes())
                )
        return value

    def validate_spells(self, value):
        try:
            spells = Spell.objects.filter(pk__in=[spell["id"] for spell in value])
        except KeyError:
            raise serializers.ValidationError(constants.RELATED_DOES_NOT_CONTAIN_ID)

        if len(spells) != len(value):
            raise serializers.ValidationError(constants.SPELLBOOK_SPELL_NOT_FOUND_ERROR)

        return spells

    def validate(self, data):
        if data.get("classes"):
            classes = set(data.get("classes"))
        else:
            classes = (
                set(self.instance.classes) if getattr(self, "instance", None) else {}
            )

        if data.get("spells"):
            spells = data.get("spells")
        else:
            spells = self.instance.spells.all() if getattr(self, "instance", None) else []

        for spell in spells:
            if not classes.intersection(set(spell.classes)):
                raise serializers.ValidationError(
                    {"spells": constants.SPELLBOOK_SPELL_CLASS_VALIDATION_ERROR}
                )

        return data

    @transaction.atomic
    def create(self, validated_data):
        sb_service = SpellbookService.create(validated_data)

        return sb_service.spellbook

    @transaction.atomic
    def update(self, spellbook, validated_data):
        validated_spells = validated_data.pop("spells", [])
        sb_service = SpellbookService(spellbook)

        # Handle updates to the spellbook and spell list w/ validation
        sb_service.update_spellbook(validated_data)
        sb_service.reconcile_spellbook_spells(validated_spells)

        return sb_service.spellbook
