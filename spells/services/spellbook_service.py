from collections import OrderedDict
from typing import Iterable, Union, Dict
from spells.models import Spellbook


class SpellbookService:
    """An object used to interact with the spellbook data layer"""

    def __init__(self, spellbook):
        self.spellbook = spellbook

    @classmethod
    def create(cls, validated_data: dict):
        spellbook = Spellbook()
        spells = validated_data.pop("spells", [])
        sb_service = cls(spellbook)
        sb_service.update_spellbook(validated_data)
        sb_service.add_spells(spells)
        return sb_service

    def add_spells(self, spells: Iterable):
        """Add spells from iterable to spellbook"""
        self.spellbook.spells.add(*spells)

    def remove_spells(self, spells: Iterable):
        """Remove spells in iterable from spellbook"""
        self.spellbook.spells.remove(*spells)

    def update_spellbook(self, data: Union[Dict, OrderedDict]):
        """Updates and saves a spellbook with attributes from data"""
        for (key, value) in data.items():
            setattr(self.spellbook, key, value)
        self.spellbook.save()

    def reconcile_spellbook_spells(self, spells: Iterable) -> dict:
        """Reconciles the spellbook's current spells with the list of incoming spells and classes
        
        Arguments:
            spells {Iterable} -- The definitive list of new spellbook spells

        Returns:
            dict -- Contains newly added and removed spells
        """

        spells = set(spells)
        current_spells = set(self.spellbook.spells.all())
        spells_to_add = spells.difference(current_spells)
        spells_to_remove = current_spells.difference(spells)

        self.add_spells(spells_to_add)
        self.remove_spells(spells_to_remove)

        return {"added": list(spells_to_add), "removed": list(spells_to_remove)}
