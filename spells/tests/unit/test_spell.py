from django.test import TestCase
from spells.models.spell import Spell


class SpellModelTestCase(TestCase):
    def setUp(self):
        Spell.objects.create(
            name="Acid Splash",
            level=0,
            description="You hurl a bubble of acid.",
            school="conjuration",
            ritual=False,
            castime_time="1 action",
            components={"raw": "V, S"},
            classes=['sorcerer', 'wizard'],
            spell_range="60 feet",
            duration="Instantaneous",
            spell_type="Conjuration cantrip",
        )
