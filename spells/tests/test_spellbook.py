from dnd_spellbook.utils import constants as const
from spells.tests.base import APITestCase
from spells.models.spell import Spell
from spells.models.spellbook import Spellbook


class SpellbookListTestCase(APITestCase):
    def setUp(self):
        super(SpellbookListTestCase, self).setUp()

        self.spellbook = Spellbook.objects.create(
            name="Gelabrous Finn",
            description="Healbot McHeals",
            classes=["cleric"],
            user=self.user
        )
        self.spellbook.spells.set(Spell.objects.filter(classes__contains=["cleric"], level__lte=2))

    def test_spellbook_list(self):
        response = self.client.get('/api/spellbooks/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['name'], self.spellbook.name)
        self.assertIsNotNone(response.data['results'][0].pop('spells', None))

    def test_spellbook_list_hide_spells(self):
        response = self.client.get('/api/spellbooks/?hide_spells=true')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['name'], self.spellbook.name)
        self.assertIsNone(response.data['results'][0].pop('spells', None))


class SpellbookRetrieveTestCase(APITestCase):
    def setUp(self):
        super(SpellbookRetrieveTestCase, self).setUp()

        self.spellbook = Spellbook.objects.create(
            name="Gelabrous Finn",
            description="Healbot McHeals",
            classes=["cleric"],
            user=self.user
        )
        self.spellbook.spells.set(Spell.objects.filter(classes__contains=["cleric"], level__lte=2))

    def test_spellbook_retrieve(self):
        response = self.client.get('/api/spellbooks/{}/'.format(self.spellbook.pk))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.spellbook.name)
        self.assertIsNotNone(response.data.pop('spells', None))

    def test_spellbook_retrieve_hide_spells(self):
        response = self.client.get('/api/spellbooks/{}/?hide_spells=true'.format(self.spellbook.pk))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.spellbook.name)
        self.assertIsNone(response.data.pop('spells', None))

    def test_cannot_view_spellbook_owned_by_another_user(self):
        self.client.force_authenticate(user=self.secondary_user)
        response = self.client.get('/api/spellbooks/{}/'.format(self.spellbook.pk))

        self.assertEqual(response.status_code, 404)


class SpellbookCreateTestCase(APITestCase):
    def setUp(self):
        super(SpellbookCreateTestCase, self).setUp()

        self.spellbook_data = {
            'name': "Daz Doodle",
            'description': "Gnome sorcerer's are better",
            'classes': [
                "sorcerer"
            ],
            'spells': [
                {'id': 1},
                {'id': 33}
            ]
        }

    def test_spellbook_create(self):
        response = self.client.post('/api/spellbooks/', self.spellbook_data, 'json')
        response_ids = [spell['id'] for spell in response.data['spells']]
        spellbook_data_ids = [spell['id'] for spell in self.spellbook_data['spells']]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], self.spellbook_data['name'])
        self.assertIsNotNone(response.data.get('spells', None))
        self.assertEqual(response_ids, spellbook_data_ids)

    def test_spellbook_create_spell_not_found(self):
        self.spellbook_data['spells'] = [{'id': 1234567}]
        response = self.client.post('/api/spellbooks/', self.spellbook_data, 'json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['spells'][0], const.SPELLBOOK_SPELL_NOT_FOUND_ERROR)

    def test_spellbook_create_spell_class_invalid(self):
        self.spellbook_data['spells'] = [{
            'id': Spell.objects.exclude(classes__contains=self.spellbook_data['classes']).first().pk
        }]
        response = self.client.post('/api/spellbooks/', self.spellbook_data, 'json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['spells'][0], const.SPELLBOOK_SPELL_CLASS_VALIDATION_ERROR)

    def test_spellbook_create_spell_has_no_id(self):
        self.spellbook_data['spells'] = [{}]
        response = self.client.post('/api/spellbooks/', self.spellbook_data, 'json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['spells'][0], const.SPELL_DOES_NOT_CONTAIN_ID)


class SpellbookUpdateTestCase(APITestCase):
    def setUp(self):
        super(SpellbookUpdateTestCase, self).setUp()

        self.spellbook = Spellbook.objects.create(
            name="Gelabrous Finn",
            description="Healbot McHeals",
            classes=["cleric"],
            user=self.user
        )
        self.spellbook.spells.set(Spell.objects.filter(classes__contains=["cleric"], level__lte=2)[:10])

    def test_spellbook_simple_update(self):
        update_data = {'name': "Brock Grillz", 'description': "Coolest name ever!"}
        response = self.client.patch('/api/spellbooks/{}/'.format(self.spellbook.pk), update_data, 'json')
        self.spellbook.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        for key in update_data:
            self.assertEqual(response.data[key], update_data[key])
            self.assertEqual(response.data[key], getattr(self.spellbook, key))

    def test_spellbook_spell_update(self):
        spell_to_add = Spell.objects.filter(classes__contains=["cleric"], level=3).first()
        update_data = {'spells': [{'id': spell_to_add.pk}]}
        response = self.client.patch('/api/spellbooks/{}/'.format(self.spellbook.pk), update_data, 'json')
        self.spellbook.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertIn(spell_to_add.pk, [spell['id'] for spell in response.data['spells']])
        self.assertIn(spell_to_add.pk, [spell.pk for spell in self.spellbook.spells.all()])

    def test_spellbook_class_update(self):
        update_data = {'classes': ['paladin']}
        response = self.client.patch('/api/spellbooks/{}/'.format(self.spellbook.pk), update_data, 'json')
        self.spellbook.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['classes'], self.spellbook.classes)
        self.assertFalse(
            self.spellbook.spells.exclude(
                classes__contains=update_data['classes']).filter(
                classes__contains=['cleric']).exists()
        )

    def test_spellbook_spell_with_removals_update(self):
        removed_spell_ids = [spell.id for spell in self.spellbook.spells.all()[:5]]
        new_spell_list = [{'id': spell['id']} for spell in self.spellbook.spells.all()[5:10].values('id')]
        update_data = {'spells': new_spell_list}
        response = self.client.patch('/api/spellbooks/{}/'.format(self.spellbook.pk), update_data, 'json')
        self.spellbook.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['spells']), len(new_spell_list))
        for spell in response.data['spells']:
            self.assertNotIn(spell['id'], removed_spell_ids)

    def test_spellbook_update_spell_not_found(self):
        update_data = {'spells': [{'id': 1234567}]}
        response = self.client.patch('/api/spellbooks/{}/'.format(self.spellbook.pk), update_data, 'json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['spells'][0], const.SPELLBOOK_SPELL_NOT_FOUND_ERROR)

    def test_spellbook_update_spell_class_invalid(self):
        update_data = {'spells': [{
            'id': Spell.objects.exclude(classes__contains=self.spellbook.classes).first().pk
        }]}
        response = self.client.patch('/api/spellbooks/{}/'.format(self.spellbook.pk), update_data, 'json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['spells'][0], const.SPELLBOOK_SPELL_CLASS_VALIDATION_ERROR)

    def test_spellbook_create_spell_has_no_id(self):
        update_data = {'spells': [{}]}
        response = self.client.patch('/api/spellbooks/{}/'.format(self.spellbook.pk), update_data, 'json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['spells'][0], const.SPELL_DOES_NOT_CONTAIN_ID)

    def test_cannot_update_spellbook_owned_by_another_user(self):
        update_data = {'name': "Brock Grillz"}
        self.client.force_authenticate(user=self.secondary_user)
        response = self.client.patch('/api/spellbooks/{}/'.format(self.spellbook.pk), update_data, 'json')

        self.assertEqual(response.status_code, 404)


class SpellbookDestroyTestCase(APITestCase):
    def setUp(self):
        super(SpellbookDestroyTestCase, self).setUp()

        self.spellbook = Spellbook.objects.create(
            name="Gelabrous Finn",
            description="Healbot McHeals",
            classes=["cleric"],
            user=self.user
        )
        self.spellbook.spells.set(Spell.objects.filter(classes__contains=["cleric"], level__lte=2)[:10])
        self.pk_to_destroy = self.spellbook.pk

    def test_spellbook_destroy(self):
        response = self.client.delete('/api/spellbooks/{}/'.format(self.spellbook.pk))

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Spellbook.DoesNotExist):
            Spellbook.objects.get(pk=self.pk_to_destroy)

    def test_cannot_destroy_spellbook_owned_by_another_user(self):
        self.client.force_authenticate(user=self.secondary_user)
        response = self.client.delete('/api/spellbooks/{}/'.format(self.spellbook.pk))

        self.assertEqual(response.status_code, 404)
