from rest_framework.viewsets import ModelViewSet

from core.models import Tamanho
from core.serializers import TamanhoSerializer, TamanhoListSerializer, TamanhoRetrieveSerializer

class TamanhoViewSet(ModelViewSet):
    queryset = Tamanho.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list":
            return TamanhoListSerializer
        elif self.action == "retrieve":
            return TamanhoRetrieveSerializer
        return TamanhoSerializer
