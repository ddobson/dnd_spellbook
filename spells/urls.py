from django.urls import include, re_path
from spells.views import SpellbookView, SpellView
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'spells', SpellView, base_name="spells")
router.register(r'spellbooks', SpellbookView, base_name="spellbooks")

spellbooks_router = routers.NestedDefaultRouter(router, r'spellbooks', lookup='spellbook')
spellbooks_router.register(r'spells', SpellView,  base_name='spellbook-spells')

urlpatterns = router.urls + spellbooks_router.urls
