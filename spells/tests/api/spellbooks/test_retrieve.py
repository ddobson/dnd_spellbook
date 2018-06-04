from rest_framework import status
from spells.tests.base import APITestCase
from spells.models.spell import Spell
from spells.models.spellbook import Spellbook


class SpellbookRetrieveTestCase(APITestCase):
    def setUp(self):
        super(SpellbookRetrieveTestCase, self).setUp()

        self.spellbook = Spellbook.objects.create(
            name="Gelabrous Finn",
            description="Healbot McHeals",
            classes=['cleric'],
            user=self.user
        )
        self.spellbook.spells.set(Spell.objects.filter(classes__contains=['cleric'], level__lte=2))

    def test_spellbook_retrieve(self):
        response = self.client.get('/api/spellbooks/{}/'.format(self.spellbook.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.spellbook.name)
        self.assertIsNotNone(response.data.pop('spells', None))

    def test_spellbook_retrieve_hide_spells(self):
        response = self.client.get('/api/spellbooks/{}/?hide_spells=true'.format(self.spellbook.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.spellbook.name)
        self.assertIsNone(response.data.pop('spells', None))

    def test_cannot_view_spellbook_owned_by_another_user(self):
        self.client.force_authenticate(user=self.secondary_user)
        response = self.client.get('/api/spellbooks/{}/'.format(self.spellbook.pk))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
