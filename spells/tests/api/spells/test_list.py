from spells.tests.base import APITestCase
from spells.models import Spell


class SpellListTestCase(APITestCase):
    def test_spell_list(self):
        spells = Spell.objects.all()[:50]  # Default pagination limit is 50
        response = self.client.get("/api/spells/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), len(spells))

    def test_spell_list_with_classes_query(self):
        response = self.client.get("/api/spells/?classes=paladin")

        self.assertEqual(response.status_code, 200)
        for spell in response.data["results"]:
            self.assertTrue("paladin" in spell["classes"])

    def test_spell_list_with_multiple_classes_query(self):
        response = self.client.get("/api/spells/?classes=paladin,ranger")

        self.assertEqual(response.status_code, 200)
        for spell in response.data["results"]:
            self.assertTrue("paladin" in spell["classes"] or "ranger" in spell["classes"])
