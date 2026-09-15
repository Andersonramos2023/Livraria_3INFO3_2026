from pyexpat import model
from attr import field
from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField
from core.models import Compra, ItensCompra
from django.db import transaction

class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade')


class CompraCreateUpdateSerializer(ModelSerializer):
    itens = ItensCompraCreateUpdateSerializer(many=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')

    @transaction.atomic
    def create(self, validated_data):
        itens = validated_data.pop('itens')
        compra = Compra.objects.create(**validated_data)
        for item in itens:
            ItensCompra.objects.create(compra=compra, **item)
        compra.save()
        return compra
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
