from venv import create
from rest_framework.viewsets import ModelViewSet
from core.serializers import CompraCreateUpdateSerializer, CompraListSerializer,CompraSerializer
from core.models import Compra


class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.order_by('-id')
    serializer_class = CompraSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompraListSerializer
        if self.action in {'create', 'update'}:
            return CompraCreateUpdateSerializer
        return CompraSerializer
