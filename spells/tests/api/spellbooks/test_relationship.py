from rest_framework import status
from spells.tests.base import APITestCase
from spells.models import Spell
from spells.models import Spellbook


class SpellbookSpellRelationshipTestCase(APITestCase):
    def setUp(self):
        super(SpellbookSpellRelationshipTestCase, self).setUp()

        self.spellbook = Spellbook.objects.create(
            name="Gelabrous Finn",
            description="Healbot McHeals",
            classes=["cleric"],
            user=self.user,
        )
        self.spell = Spell.objects.filter(classes__contains=["cleric"]).first()

    def test_spellbook_spell_add(self):
        response = self.client.post(
            "/api/spellbooks/{}/spells/{}/relationship/".format(
                self.spellbook.pk, self.spell.pk
            )
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.spellbook.spells.filter(pk=self.spell.pk).count(), 1)

    def test_spellbook_spell_remove(self):
        self.spellbook.spells.add(self.spell)
        response = self.client.delete(
            "/api/spellbooks/{}/spells/{}/relationship/".format(
                self.spellbook.pk, self.spell.pk
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.spellbook.spells.filter(pk=self.spell.pk).count(), 0)

    def test_spellbook_spell_add_spellbook_not_found(self):
        response = self.client.delete(
            "/api/spellbooks/{}/spells/{}/relationship/".format(1234567890, self.spell.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.spellbook.spells.filter(pk=self.spell.pk).count(), 0)

    def test_spellbook_spell_remove_spellbook_not_found(self):
        self.spellbook.spells.add(self.spell)
        response = self.client.delete(
            "/api/spellbooks/{}/spells/{}/relationship/".format(1234567890, self.spell.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.spellbook.spells.filter(pk=self.spell.pk).count(), 1)

    def test_spellbook_spell_add_spell_not_found(self):
        response = self.client.delete(
            "/api/spellbooks/{}/spells/{}/relationship/".format(
                self.spellbook.pk, 1234567890
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Spell not found")
        self.assertEqual(self.spellbook.spells.filter(pk=self.spell.pk).count(), 0)

    def test_spellbook_spell_remove_spell_not_found(self):
        self.spellbook.spells.add(self.spell)
        response = self.client.delete(
            "/api/spellbooks/{}/spells/{}/relationship/".format(
                self.spellbook.pk, 1234567890
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Spell not found")
        self.assertEqual(self.spellbook.spells.filter(pk=self.spell.pk).count(), 1)

    def test_cannot_add_spell_for_spellbook_owned_by_another_user(self):
        self.client.force_authenticate(user=self.secondary_user)
        response = self.client.post(
            "/api/spellbooks/{}/spells/{}/relationship/".format(
                self.spellbook.pk, self.spell.pk
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_remove_spell_for_spellbook_owned_by_another_user(self):
        self.spellbook.spells.add(self.spell)
        self.client.force_authenticate(user=self.secondary_user)
        response = self.client.delete(
            "/api/spellbooks/{}/spells/{}/relationship/".format(
                self.spellbook.pk, self.spell.pk
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.spellbook.spells.filter(pk=self.spell.pk).count(), 1)
