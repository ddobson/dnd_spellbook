from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Spell
from .models import Spellbook
from .serializers import SpellbookSerializer, SpellSerializer
from .services.spellbook_service import SpellbookService


class SpellbookView(ModelViewSet):
    serializer_class = SpellbookSerializer

    def get_queryset(self):
        return Spellbook.objects.filter(user=self.request.user)


class SpellView(ReadOnlyModelViewSet):
    serializer_class = SpellSerializer

    def get_queryset(self):
        spells = Spell.objects.order_by("level", "name")
        class_params = self.request.GET.get("classes")
        classes = class_params.split(",") if class_params else None
        return spells.filter(classes__overlap=classes) if classes else spells


class NestedSpellView(SpellView):
    def get_queryset(self):
        # Return a 404 if the requesting user does not own the spellbook
        spellbook = get_object_or_404(
            Spellbook, pk=self.kwargs["spellbook_pk"], user=self.request.user
        )
        spells = super(NestedSpellView, self).get_queryset()
        return spells.filter(spellbooks=spellbook.pk)

    @action(methods=["post", "delete"], detail=True)
    def relationship(self, request, spellbook_pk=None, pk=None):
        spellbook = get_object_or_404(Spellbook, pk=spellbook_pk, user=self.request.user)
        spell = get_object_or_404(Spell, pk=pk)
        sb_service = SpellbookService(spellbook)

        if request.method == "POST":
            sb_service.add_spells([spell])
            return Response(status=201)

        sb_service.remove_spells([spell])
        return Response(status=204)


class SpellbookSpellPdf(View):
    def get(self, request, id):
        spellbook = get_object_or_404(Spellbook, pk=id)
        context = {"spellbook": spellbook}

        return render(request, "spellbook_pdf.html", context)
