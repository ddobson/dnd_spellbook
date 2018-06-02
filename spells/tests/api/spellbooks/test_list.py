from rest_framework import status
from spells.tests.base import APITestCase
from spells.models.spell import Spell
from spells.models.spellbook import Spellbook


class SpellbookListTestCase(APITestCase):
    def setUp(self):
        super(SpellbookListTestCase, self).setUp()

        self.spellbook = Spellbook.objects.create(
            name="Gelabrous Finn",
            description="Healbot McHeals",
            classes=['cleric'],
            user=self.user
        )
        self.spellbook.spells.set(Spell.objects.filter(classes__contains=['cleric'], level__lte=2))

    def test_spellbook_list(self):
        response = self.client.get('/api/spellbooks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], self.spellbook.name)
        self.assertIsNotNone(response.data['results'][0].pop('spells', None))

    def test_spellbook_list_hide_spells(self):
        response = self.client.get('/api/spellbooks/?hide_spells=true')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], self.spellbook.name)
        self.assertIsNone(response.data['results'][0].pop('spells', None))
