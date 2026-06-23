from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField, ModelSerializer

from core.models import Compra

class CompraSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    
class CompraSerializer(ModelSerializer):
    status = CharField(source='get_status_display', read_only=True)

class CompraSerializer(ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'