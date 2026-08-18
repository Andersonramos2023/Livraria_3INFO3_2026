from pyexpat import model
from attr import field
from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField
from core.models import Compra, ItensCompra


class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade
    class Meta:
        model = ItensCompra

    fields = ('livro', 'quantidade')
    Depth = 1


class CompraSerializer(ModelSerializer):
    class Meta:
        model = Compra
        itens = ItensCompraSerializer(many=True, read_only=True)
        fields = '__all__'

    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
