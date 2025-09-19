
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


from core.models import Tamanho
from core.serializers import TamanhoSerializer, TamanhoListSerializer, TamanhoRetrieveSerializer




class TamanhoViewSet(ModelViewSet):
   queryset = Tamanho.objects.all()
   filter_backends = [DjangoFilterBackend]
   filterset_fields = ['categoria__id'] 


   def get_serializer_class(self):
       if self.action == "list":
           return TamanhoListSerializer
       elif self.action == "retrieve":
           return TamanhoRetrieveSerializer
       return TamanhoSerializer