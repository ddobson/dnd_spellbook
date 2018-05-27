from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from spells.models.spell import Spell
from spells.models.spellbook import Spellbook
from spells.serializers import SpellbookSerializer, SpellSerializer


class SpellbookView(ModelViewSet):
    serializer_class = SpellbookSerializer

    def get_queryset(self):
        return Spellbook.objects.filter(user=self.request.user)

    def create(self, request):
        return super(SpellbookView, self).create(request)

    def update(self, request, pk=None, partial=None):
        return super(SpellbookView, self).update(request, pk, partial)


class SpellView(ReadOnlyModelViewSet):
    serializer_class = SpellSerializer

    def get_queryset(self):
        spells = Spell.objects.all()
        class_params = self.request.GET.get('classes')
        classes = class_params.split(',') if class_params else None

        return spells.filter(classes__overlap=classes) if classes else spells


class NestedSpellView(SpellView):
    def get_queryset(self):
        spells = super(NestedSpellView, self).get_queryset()

        return spells.filter(spellbooks=self.kwargs['spellbook_pk'])
