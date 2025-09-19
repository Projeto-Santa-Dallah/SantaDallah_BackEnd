from rest_framework.viewsets import ModelViewSet


from core.models import Produto
from core.serializers import ProdutoSerializer, ProdutoRetrieveSerializer, ProdutoListSerializer
from django_filters.rest_framework import DjangoFilterBackend
class ProdutoViewSet(ModelViewSet):
   queryset = Produto.objects.all()
   filter_backends = [DjangoFilterBackend]
   filterset_fields = ['categoria__id']
  
   def get_serializer_class(self):
       if self.action == "list":
           return ProdutoListSerializer
       elif self.action == "retrieve":
           return ProdutoRetrieveSerializer
       return ProdutoSerializer