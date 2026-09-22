from pyexpat import model
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    CurrentUserDefault,
    HiddenField,
    SerializerMethodField,
    ValidationError,
)
from core.models import Compra, ItensCompra
from django.db import transaction


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade')

    def validate(self, item):
        if item['quantidade'] > item['livro'].quantidade:
            raise ValidationError('Quantidade de itens maior do que a quantidade em estoque.')
        return item


class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'livro')
        depth = 1


class CompraCreateUpdateSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')

    @transaction.atomic
    def update(self, compra, validated_data):
        itens = validated_data.pop('itens', None)
        if itens is not None:
            compra.itens.all().delete()
            for item in itens:
                ItensCompra.objects.create(compra=compra, **item)
        return super().update(compra, validated_data)


class CompraListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensCompraListSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')


class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade

    class Meta:
        model = ItensCompra
        fields = ('id', 'usuario', 'status', 'total', 'itens')
        depth = 1


class CompraSerializer(ModelSerializer):
    class Meta:
        model = Compra
        itens = ItensCompraSerializer(many=True, read_only=True)
        fields = '__all__'

    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
