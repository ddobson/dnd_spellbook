from spells.tests.base import APITestCase
from spells.models import Spell


class SpellRetrieveTestCase(APITestCase):
    def test_spell_list(self):
        spell = Spell.objects.get(pk=1)
        response = self.client.get("/api/spells/1/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], spell.name)
