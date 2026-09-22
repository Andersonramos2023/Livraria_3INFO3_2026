from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from core.models import Livro
from core.serializers import (
    LivroAlterarPrecoSerializer,
    LivroListSerializer,
    LivroRetrieveSerializer,
    LivroSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria__descricao', 'editora__nome']  # Campos para filtragem


class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return LivroListSerializer
        elif self.action == 'retrieve':
            return LivroRetrieveSerializer
        return LivroSerializer

    @extend_schema(
        request=LivroAlterarPrecoSerializer,
        responses={200: None},
        description='Altera o preço de um livro específico.',
        summary='Alterar preço do livro',
    )
    @action(detail=True, methods=['patch'])
    def alterar_preco(self, request, pk=None):

        @action(detail=True, methods=['patch'])
        def alterar_preco(self, request, pk=None):
            livro = self.get_object()

            serializer = LivroAlterarPrecoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            livro.preco = serializer.validated_data['preco']
            livro.save()

            return Response(
                {'detail': f'Preço do livro "{livro.titulo}" atualizado para {livro.preco}.'}, status=status.HTTP_200_OK
            )
