from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


from core.models import Categoria
from core.serializers import CategoriaSerializer


class CategoriaViewSet(ModelViewSet):
   queryset = Categoria.objects.all()
   serializer_class = CategoriaSerializer
   filter_backends = [DjangoFilterBackend]
   filterset_fields = ['id', 'nome']  # já permite ?id=1 ou ?nome=XYZ