from rest_framework.viewsets import (ModelViewSet, ReadOnlyModelViewSet)
from spells.models import (Spellbook, Spell)
from spells.serializers import (SpellbookSerializer, SpellSerializer)


class SpellbookView(ModelViewSet):
    serializer_class = SpellbookSerializer

    def get_queryset(self):
        return Spellbook.objects.filter(user=self.request.user)


class SpellView(ReadOnlyModelViewSet):
    serializer_class = SpellSerializer

    def get_queryset(self):
        spells = Spell.objects.all()
        class_params = self.request.GET.get('classes')
        classes = class_params.split(',') if class_params else None

        return spells.filter(classes__overlap=classes) if classes else spells
