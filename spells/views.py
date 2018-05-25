from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
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
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except (Spell.DoesNotExist, ValidationError) as error:
            if isinstance(error, Spell.DoesNotExist):
                error_message = "Spell does not exist."
            else:
                error_message = error.message

            return Response(
                data={'error': error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(methods=['post'], detail=True)
    def add_spell(self, request, pk=None):
        return self._add_or_remove_spell(request, 'add')

    @action(methods=['delete'], detail=True)
    def remove_spell(self, request, pk=None):
        return self._add_or_remove_spell(request, 'remove')

    def _add_or_remove_spell(self, request, action):
        spellbook = self.get_object()

        try:
            spell = Spell.objects.get(pk=request.data['id'])
            if action == 'add':
                spellbook.spells.add(spell)
                return Response(status=status.HTTP_201_CREATED)
            elif action == 'remove':
                spellbook.spells.remove(spell)
                return Response(status=status.HTTP_204_NO_CONTENT)
        except (Spell.DoesNotExist, ValidationError) as error:
            if isinstance(error, Spell.DoesNotExist):
                error_message = "Spell with ID `{}` does not exist.".format(request.data['id'])
            else:
                error_message = error.message

            return Response(
                data={'error': error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SpellView(ReadOnlyModelViewSet):
    serializer_class = SpellSerializer

    def get_queryset(self):
        spells = Spell.objects.filter(spellbooks=self.kwargs['spellbook_pk'])
        class_params = self.request.GET.get('classes')
        classes = class_params.split(',') if class_params else None

        return spells.filter(classes__overlap=classes) if classes else spells

# Try with new SpellbookSpellView and see if POST can be made to work
