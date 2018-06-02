from rest_framework import status
from spells.tests.base import APITestCase
from spells.models.spell import Spell
from spells.models.spellbook import Spellbook


class SpellbookSpellRetrieveTestCase(APITestCase):
    def setUp(self):
        super(SpellbookSpellRetrieveTestCase, self).setUp()

        self.spellbook = Spellbook.objects.create(
            name="Gelabrous Finn",
            description="Healbot McHeals",
            classes=['cleric'],
            user=self.user
        )
        self.spellbook.spells.set(Spell.objects.filter(classes__contains=['cleric'], level__lte=2)[:10])
        self.spell = self.spellbook.spells.first()

    def test_spellbook_spell_retrieve(self):
        response = self.client.get('/api/spellbooks/{}/spells/{}/'.format(self.spellbook.pk, self.spell.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.spell.pk)

    def test_cannot_view_spell_for_spellbook_owned_by_another_user(self):
        self.client.force_authenticate(user=self.secondary_user)
        response = self.client.get('/api/spellbooks/{}/spells/{}/'.format(self.spellbook.pk, self.spell.pk))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
