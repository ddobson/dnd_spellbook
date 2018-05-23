from rest_framework import viewsets
from spells.models import Spell
from spells.serializers import SpellSerializer


class SpellViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Spell.objects.all()
    serializer_class = SpellSerializer
