from django.test import TestCase
from rest_framework.test import APIClient

from spells.models import Spell
from user.models import User


class APITestCase(TestCase):
    fixtures = ('spells.json', 'users.json')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=User.objects.first())


class SpellListTestCase(APITestCase):
    def test_spell_list(self):
        spells = Spell.objects.all()[:50]  # Default pagination limit is 50
        response = self.client.get('/api/spells/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), len(spells))

    def test_spell_list_with_classes_query(self):
        response = self.client.get('/api/spells/?classes=paladin')

        self.assertEqual(response.status_code, 200)
        for spell in response.data['results']:
            self.assertTrue('paladin' in spell['classes'])

    def test_spell_list_with_multiple_classes_query(self):
        response = self.client.get('/api/spells/?classes=paladin,ranger')

        self.assertEqual(response.status_code, 200)
        for spell in response.data['results']:
            self.assertTrue('paladin' in spell['classes'] or 'ranger' in spell['classes'])


class SpellRetrieveTestCase(APITestCase):
    def test_spell_list(self):
        spell = Spell.objects.get(pk=1)
        response = self.client.get('/api/spells/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], spell.name)
