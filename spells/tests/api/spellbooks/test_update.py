from dnd_spellbook import constants as const
from rest_framework import status
from spells.tests.base import APITestCase
from spells.models import Spell
from spells.models import Spellbook


class SpellbookUpdateTestCase(APITestCase):
    def setUp(self):
        super(SpellbookUpdateTestCase, self).setUp()

        self.spellbook = Spellbook.objects.create(
            name="Gelabrous Finn",
            description="Healbot McHeals",
            classes=["cleric"],
            user=self.user,
        )
        self.spellbook.spells.set(
            Spell.objects.filter(classes__contains=["cleric"], level__lte=2)[:10]
        )

    def test_spellbook_simple_update(self):
        update_data = {"name": "Brock Grillz", "description": "Coolest name ever!"}
        response = self.client.patch(
            "/api/spellbooks/{}/".format(self.spellbook.pk), update_data, "json"
        )
        self.spellbook.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in update_data:
            self.assertEqual(response.data[key], update_data[key])
            self.assertEqual(response.data[key], getattr(self.spellbook, key))

    def test_spellbook_spell_update(self):
        spell_to_add = Spell.objects.filter(classes__contains=["cleric"], level=3).first()
        update_data = {"spells": [{"id": spell_to_add.pk}]}
        response = self.client.patch(
            "/api/spellbooks/{}/".format(self.spellbook.pk), update_data, "json"
        )
        self.spellbook.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(spell_to_add.pk, [spell["id"] for spell in response.data["spells"]])
        self.assertIn(
            spell_to_add.pk, [spell.pk for spell in self.spellbook.spells.all()]
        )

    def test_spellbook_class_update(self):
        update_data = {"classes": ["paladin"]}
        response = self.client.patch(
            "/api/spellbooks/{}/".format(self.spellbook.pk), update_data, "json"
        )
        self.spellbook.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["classes"], self.spellbook.classes)
        self.assertFalse(
            self.spellbook.spells.exclude(classes__contains=update_data["classes"])
            .filter(classes__contains=["cleric"])
            .exists()
        )

    def test_spellbook_spell_with_removals_update(self):
        removed_spell_ids = [spell.id for spell in self.spellbook.spells.all()[:5]]
        new_spell_list = [
            {"id": spell["id"]}
            for spell in self.spellbook.spells.all()[5:10].values("id")
        ]
        update_data = {"spells": new_spell_list}
        response = self.client.patch(
            "/api/spellbooks/{}/".format(self.spellbook.pk), update_data, "json"
        )
        self.spellbook.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["spells"]), len(new_spell_list))
        for spell in response.data["spells"]:
            self.assertNotIn(spell["id"], removed_spell_ids)

    def test_spellbook_update_spell_not_found(self):
        update_data = {"spells": [{"id": 1234567}]}
        response = self.client.patch(
            "/api/spellbooks/{}/".format(self.spellbook.pk), update_data, "json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["spells"][0], const.SPELLBOOK_SPELL_NOT_FOUND_ERROR
        )

    def test_spellbook_update_spell_class_invalid(self):
        update_data = {
            "spells": [
                {
                    "id": Spell.objects.exclude(classes__contains=self.spellbook.classes)
                    .first()
                    .pk
                }
            ]
        }
        response = self.client.patch(
            "/api/spellbooks/{}/".format(self.spellbook.pk), update_data, "json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["spells"][0], const.SPELLBOOK_SPELL_CLASS_VALIDATION_ERROR
        )

    def test_spellbook_create_spell_has_no_id(self):
        update_data = {"spells": [{}]}
        response = self.client.patch(
            "/api/spellbooks/{}/".format(self.spellbook.pk), update_data, "json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["spells"][0], const.SPELL_DOES_NOT_CONTAIN_ID)

    def test_cannot_update_spellbook_owned_by_another_user(self):
        update_data = {"name": "Brock Grillz"}
        self.client.force_authenticate(user=self.secondary_user)
        response = self.client.patch(
            "/api/spellbooks/{}/".format(self.spellbook.pk), update_data, "json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
