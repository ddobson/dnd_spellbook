from rest_framework import status
from spells.tests.base import APITestCase
from spells.models.spell import Spell
from spells.models.spellbook import Spellbook


class SpellbookSpellListTestCase(APITestCase):
    def setUp(self):
        super(SpellbookSpellListTestCase, self).setUp()

        self.spellbook = Spellbook.objects.create(
            name="Gelabrous Finn",
            description="Healbot McHeals",
            classes=['cleric'],
            user=self.user
        )
        self.spellbook.spells.set(Spell.objects.filter(classes__contains=['cleric'], level__lte=2)[:10])

    def test_spellbook_spell_list(self):
        response = self.client.get('/api/spellbooks/{}/spells/'.format(self.spellbook.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']), self.spellbook.spells.count())

    def test_cannot_view_spells_for_spellbook_owned_by_another_user(self):
        self.client.force_authenticate(user=self.secondary_user)
        response = self.client.get('/api/spellbooks/{}/spells/'.format(self.spellbook.pk))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
