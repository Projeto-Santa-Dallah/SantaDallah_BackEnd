from rest_framework.viewsets import ModelViewSet

from core.models import PrecoQuantidade
from core.serializers import PrecoQtdSerializer, PrecoQtdRetrieveSerializer, PrecoQtdListSerializer

class PrecoQtdViewSet(ModelViewSet):
    queryset = PrecoQuantidade.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PrecoQtdListSerializer
        elif self.action == 'retrieve':
            return PrecoQtdRetrieveSerializer
        return PrecoQtdSerializer