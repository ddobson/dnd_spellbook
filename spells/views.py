from django.shortcuts import get_object_or_404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from spells.models.spell import Spell
from spells.models.spellbook import Spellbook
from spells.serializers import SpellbookSerializer, SpellSerializer


class SpellbookView(ModelViewSet):
    serializer_class = SpellbookSerializer

    def get_queryset(self):
        return Spellbook.objects.filter(user=self.request.user)


class SpellView(ReadOnlyModelViewSet):
    serializer_class = SpellSerializer

    def get_queryset(self):
        spells = Spell.objects.all().order_by('level', 'name')
        class_params = self.request.GET.get('classes')
        classes = class_params.split(',') if class_params else None
        return spells.filter(classes__overlap=classes) if classes else spells


class NestedSpellView(SpellView):
    spellbook = None

    def get_queryset(self):
        # Return a 404 if the requesting user does not own the spellbook
        if not self.spellbook:
            self.spellbook = get_object_or_404(Spellbook, pk=self.kwargs['spellbook_pk'], user=self.request.user)
        spells = super(NestedSpellView, self).get_queryset()
        return spells.filter(spellbooks=self.spellbook.pk)

    @action(methods=['post', 'delete'], detail=True)
    def relationship(self, request, spellbook_pk=None, pk=None):
        self.spellbook = get_object_or_404(Spellbook, pk=spellbook_pk, user=self.request.user)
        spells = Spell.objects.filter(pk=pk)

        if spells.exists():
            if request.method == 'POST':
                self.spellbook.process_spellbook_spell_additions(spells)
                return Response(status=201)
            else:
                self.spellbook.process_spellbook_spell_removals(spells)
                return Response(status=204)
        else:
            raise exceptions.NotFound(detail="Spell not found")
