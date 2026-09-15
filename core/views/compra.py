from venv import create

from rest_framework.viewsets import ModelViewSet
from core.serializers import CompraCreateUpdateSerializer, CompraSerializer
from core.models import Compra


class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    def get_serializer_class(self):
        if self.action in ('creat', 'update', 'partial_update'):
            return CompraCreateUpdateSerializer
        return CompraSerializer
