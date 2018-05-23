from spells.views import (SpellbookView, SpellView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'spells', SpellView, base_name="spells")
router.register(r'spellbooks', SpellbookView, base_name="spells")

urlpatterns = router.urls
