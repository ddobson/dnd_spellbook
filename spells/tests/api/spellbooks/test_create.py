from dnd_spellbook import constants as const
from rest_framework import status
from spells.tests.base import APITestCase
from spells.models import Spell


class SpellbookCreateTestCase(APITestCase):
    def setUp(self):
        super(SpellbookCreateTestCase, self).setUp()

        self.spellbook_data = {
            "name": "Daz Doodle",
            "description": "Gnome sorcerer's are better",
            "classes": ["sorcerer"],
            "spells": [{"id": 1}, {"id": 33}],
        }

    def test_spellbook_create(self):
        response = self.client.post("/api/spellbooks/", self.spellbook_data, "json")
        response_ids = [spell["id"] for spell in response.data["spells"]]
        spellbook_data_ids = [spell["id"] for spell in self.spellbook_data["spells"]]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.spellbook_data["name"])
        self.assertIsNotNone(response.data.get("spells", None))
        self.assertEqual(response_ids, spellbook_data_ids)

    def test_spellbook_create_spell_not_found(self):
        self.spellbook_data["spells"] = [{"id": 1234567}]
        response = self.client.post("/api/spellbooks/", self.spellbook_data, "json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["spells"][0], const.SPELLBOOK_SPELL_NOT_FOUND_ERROR
        )

    def test_spellbook_create_spell_class_invalid(self):
        self.spellbook_data["spells"] = [
            {
                "id": Spell.objects.exclude(
                    classes__contains=self.spellbook_data["classes"]
                )
                .first()
                .pk
            }
        ]
        response = self.client.post("/api/spellbooks/", self.spellbook_data, "json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["spells"][0], const.SPELLBOOK_SPELL_CLASS_VALIDATION_ERROR
        )

    def test_spellbook_create_spell_has_no_id(self):
        self.spellbook_data["spells"] = [{}]
        response = self.client.post("/api/spellbooks/", self.spellbook_data, "json")

        self.assertContains(
            response,
            const.RELATED_DOES_NOT_CONTAIN_ID,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
