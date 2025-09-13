from rest_framework.viewsets import ModelViewSet

from core.models import Pedido
from core.serializers import PedidoSerializer, PedidoCreateUpdateSerializer, PedidoListSerializer


class PedidoViewSet(ModelViewSet):
   
    # serializer_class = PedidoSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PedidoListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return PedidoCreateUpdateSerializer
        return PedidoSerializer
    
    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser:
            return Pedido.objects.all()
        if usuario.groups.filter(name='admin'):
            return Pedido.objects.all()
        return Pedido.objects.filter(usuario=usuario)
    
