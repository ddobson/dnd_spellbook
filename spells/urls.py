from django.urls import include, re_path
from spells.views import SpellbookView, SpellView, NestedSpellView
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r'spells', SpellView, base_name="spells")
router.register(r'spellbooks', SpellbookView, base_name="spellbooks")

spellbooks_router = routers.NestedSimpleRouter(router, r'spellbooks', lookup='spellbook')
spellbooks_router.register(r'spells', NestedSpellView,  base_name='spellbook-spells')

urlpatterns = router.urls + spellbooks_router.urls
