from spells.views import SpellViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'spells', SpellViewSet, base_name="spells")

urlpatterns = router.urls
