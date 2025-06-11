from rest_framework.viewsets import ModelViewSet

from core.models import Produto
from core.serializers import ProdutoSerializer, ProdutoRetrieveSerializer, ProdutoListSerializer

class ProdutoViewSet(ModelViewSet):
    queryset = Produto.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list":
            return ProdutoListSerializer
        elif self.action == "retrieve":
            return ProdutoRetrieveSerializer
        return ProdutoSerializer
