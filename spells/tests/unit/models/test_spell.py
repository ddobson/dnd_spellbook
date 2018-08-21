from django.core.cache import cache
from django.test import TestCase
from spells.models import Spell


class SpellTestCase(TestCase):
    def setUp(self):
        self.spell = Spell.objects.create(
            school="conjuration",
            description="You hurl a bubble of acid. Choose one creature within range, or choose two creatures within range that are within 5 feet of each other. A target must succeed on a Dexterity saving throw or take 1d6 acid damage.\n\nThis spell's damage increases by 1d6 when you reach 5th level (2d6), 11th level (3d6), and 17th level (4d6).",
            level=0,
            ritual=False,
            casting_time="1 action",
            classes=["sorcerer", "wizard"],
            components={
                "raw": "V, S",
                "material": False,
                "verbal": True,
                "somatic": True,
            },
            spell_range="60 feet",
            duration="Instantaneous",
            spell_type="Conjuration cantrip",
            name="Acid Splash",
        )

    def test_spell_distinct_classes(self):
        dist = Spell.distinct_classes()
        self.assertCountEqual(self.spell.classes, dist)

    def test_spell_distinct_classes_bust_on_save(self):
        Spell.distinct_classes()
        self.assertIsNotNone(cache.get(Spell.DISTINCT_CLASS_CACHE_KEY))
        self.spell.save()
        self.assertIsNone(cache.get(Spell.DISTINCT_CLASS_CACHE_KEY))
