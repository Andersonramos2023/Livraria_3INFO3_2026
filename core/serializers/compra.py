from pyexpat import model
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    CurrentUserDefault,
    HiddenField,
    SerializerMethodField,
    ValidationError,
    DateTimeField,
)
from rest_framework.serializers import (
    DecimalField,
    ModelSerializer,
    Serializer,
    SlugRelatedField,
    ValidationError,
)
...
class LivroAlterarPrecoSerializer(Serializer):
    preco = DecimalField(max_digits=7, decimal_places=2)

    def validate_preco(self, preco):
        '''Valida se o preço é um valor positivo.'''
        if preco <= 0:
            raise ValidationError('O preço deve ser um valor positivo.')
        return preco
...
from core.models import Compra, ItensCompra
from django.db import transaction


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade', 'preco')

    def validate(self, item):
        if item['quantidade'] > item['livro'].quantidade:
            raise ValidationError('Quantidade de itens maior do que a quantidade em estoque.')
        return item


class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'preco', 'livro')
        depth = 1


class CompraCreateUpdateSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')

    @transaction.atomic
    def update(self, compra, validated_data):
        itens = validated_data.pop('itens')
        if itens:
            compra.itens.all().delete()
            for item in itens:
                item['preco'] = item['livro'].preco  # grava o preço histórico
                ItensCompra.objects.create(compra=compra, **item)
        compra.save()
        return super().update(compra, validated_data)


class LivroAlterarPrecoSerializer(Serializer):
    preco = DecimalField(max_digits=7, decimal_places=2)

    def validate_preco(self, preco):
        """Valida se o preço é um valor positivo."""
        if preco <= 0:
            raise ValidationError('O preço deve ser um valor positivo.')
        return preco


class CompraListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensCompraListSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')


class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.quantidade * instance.preco

    class Meta:
        model = ItensCompra
        fields = ('id', 'livro', 'quantidade', 'preco', 'total')
        depth = 1


class CompraSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    data = DateTimeField(read_only=True)  # novo campo
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'status', 'total', 'data', 'tipo_pagamento', 'itens')  # modificado
