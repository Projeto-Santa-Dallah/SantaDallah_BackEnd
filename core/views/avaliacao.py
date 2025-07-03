from rest_framework.viewsets import ModelViewSet

from core.models import Avaliacao
from core.serializers import AvaliacaoSerializer, AvaliacaoRetriveSerializer, AvaliacaoListSerializer

class AvaliacaoViewSet(ModelViewSet):
    queryset = Avaliacao.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AvaliacaoListSerializer
        elif self.action == 'retrieve':
            return AvaliacaoRetriveSerializer
        return AvaliacaoSerializer
