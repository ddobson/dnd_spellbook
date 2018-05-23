from rest_framework.viewsets import (ModelViewSet, ReadOnlyModelViewSet)
from spells.models import (Spellbook, Spell)
from spells.serializers import (SpellbookSerializer, SpellSerializer)


class SpellbookView(ModelViewSet):
    serializer_class = SpellbookSerializer

    def get_queryset(self):
        return Spellbook.objects.filter(user=self.request.user)


class SpellView(ReadOnlyModelViewSet):
    queryset = Spell.objects.all()
    serializer_class = SpellSerializer
