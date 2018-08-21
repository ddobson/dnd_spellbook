from django.test import TestCase
from spells.models import Spell, Spellbook
from spells.services.spellbook_service import SpellbookService
from users.models import User


class SpellbookServiceTestCase(TestCase):
    fixtures = ["users.json", "spells.json", "spellbooks.json"]

    def setUp(self):
        self.spellbook = Spellbook.objects.first()
        self.sb_service = SpellbookService(self.spellbook)

    def test_create(self):
        spells = Spell.objects.filter(classes__contains=["cleric"])[0:5]
        data = {
            "name": "Testy McTesterson",
            "description": "Every day I'm testin' it.",
            "classes": ["cleric"],
            "user": User.objects.first(),
            "spells": spells,
        }
        sb_service = SpellbookService.create(data)

        self.assertTrue(isinstance(sb_service.spellbook, Spellbook))
        self.assertEqual(sb_service.spellbook.name, data["name"])
        self.assertEqual(sb_service.spellbook.description, data["description"])
        self.assertCountEqual(sb_service.spellbook.classes, data["classes"])
        self.assertCountEqual(sb_service.spellbook.spells.all(), spells)

    def test_add_spells(self):
        spell = Spell.objects.first()
        self.sb_service.add_spells([spell])

        self.assertIn(spell, self.spellbook.spells.all())

    def test_remove_spells(self):
        spell = Spell.objects.first()
        self.spellbook.spells.add(spell)
        self.sb_service.remove_spells([spell])

        self.assertNotIn(spell, self.spellbook.spells.all())

    def test_update_spellbook(self):
        data = {
            "name": "Testy McTesterson",
            "description": "Every day I'm testin' it.",
            "classes": ["cleric"],
        }
        self.sb_service.update_spellbook(data)

        self.assertEqual(self.sb_service.spellbook.name, data["name"])
        self.assertEqual(self.sb_service.spellbook.description, data["description"])
        self.assertCountEqual(self.sb_service.spellbook.classes, data["classes"])

    def test_reconcile_spellbook_spells(self):
        spells = list(Spell.objects.all()[0:5])
        to_add = Spell.objects.exclude(pk__in=[s.pk for s in spells]).first()
        to_keep = spells[0:4]
        to_remove = spells[4]
        to_keep.append(to_add)
        self.spellbook.spells.add(*spells)
        diff_dict = self.sb_service.reconcile_spellbook_spells(to_keep)

        self.assertEquals(diff_dict["added"], [to_add])
        self.assertNotIn(diff_dict["removed"], [to_remove])
        self.assertCountEqual(to_keep, self.spellbook.spells.all())
