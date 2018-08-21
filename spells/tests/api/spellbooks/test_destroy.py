from rest_framework import status
from spells.tests.base import APITestCase
from spells.models import Spell
from spells.models import Spellbook


class SpellbookDestroyTestCase(APITestCase):
    def setUp(self):
        super(SpellbookDestroyTestCase, self).setUp()

        self.spellbook = Spellbook.objects.create(
            name="Gelabrous Finn",
            description="Healbot McHeals",
            classes=["cleric"],
            user=self.user,
        )
        self.spellbook.spells.set(
            Spell.objects.filter(classes__contains=["cleric"], level__lte=2)[:10]
        )
        self.pk_to_destroy = self.spellbook.pk

    def test_spellbook_destroy(self):
        response = self.client.delete("/api/spellbooks/{}/".format(self.spellbook.pk))

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Spellbook.DoesNotExist):
            Spellbook.objects.get(pk=self.pk_to_destroy)

    def test_cannot_destroy_spellbook_owned_by_another_user(self):
        self.client.force_authenticate(user=self.secondary_user)
        response = self.client.delete("/api/spellbooks/{}/".format(self.spellbook.pk))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
