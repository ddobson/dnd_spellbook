from django.urls import include, re_path
from spells import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'spells', views.SpellView, base_name='spells')
router.register(r'spellbooks', views.SpellbookView, base_name='spellbooks')

spellbooks_router = routers.NestedDefaultRouter(router, r'spellbooks', lookup='spellbook')
spellbooks_router.register(r'spells', views.NestedSpellView,  base_name='spellbook-spells')

urlpatterns = router.urls + spellbooks_router.urls
