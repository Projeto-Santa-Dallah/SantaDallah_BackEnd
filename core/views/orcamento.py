from rest_framework.viewsets import ModelViewSet

from core.models import Orcamento
from core.serializers import OrcamentoSerializer, OrcamentoRetriveSerializer, OrcamentoListSerializer

class OrcamentoViewSet(ModelViewSet):
    queryset = Orcamento.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrcamentoListSerializer
        elif self.action == 'retrieve':
            return OrcamentoRetriveSerializer
        return OrcamentoSerializer
