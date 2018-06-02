from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class Spell(models.Model):
    class Meta:
        ordering = ['id']

    casting_time = models.CharField(blank=True, null=True, max_length=128)
    classes = ArrayField(
        models.CharField(max_length=24, blank=True),
        default=list,
        size=24,
    )
    components = JSONField(default=dict)
    description = models.CharField(blank=True, null=True, max_length=10240)
    higher_levels = models.CharField(blank=True, null=True, max_length=1024)
    duration = models.CharField(blank=True, null=True, max_length=128)
    level = models.SmallIntegerField(default=0)
    name = models.CharField(blank=True, null=True, max_length=128)
    spell_range = models.CharField(blank=True, null=True, max_length=128)
    ritual = models.BooleanField(default=False)
    school = models.CharField(blank=True, null=True, max_length=128)
    spell_type = models.CharField(blank=True, null=True, max_length=128)

    @classmethod
    def spell_queryset_from_request_data(cls, validated_spell_request_data):
        spells_ids = [spell['id'] for spell in validated_spell_request_data]
        spells = cls.objects.filter(pk__in=spells_ids)
        if not spells.exists() or len(spells) != len(spells_ids):
            raise cls.DoesNotExist()
        return spells

    @classmethod
    def spell_list_from_request_data(cls, validated_spell_request_data):
        return [spell for spell in cls.spell_queryset_from_request_data(validated_spell_request_data)]
