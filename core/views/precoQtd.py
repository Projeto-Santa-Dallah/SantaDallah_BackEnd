from rest_framework.viewsets import ModelViewSet

from core.models import PrecoQuantidade
from core.serializers import PrecoQtdSerializer

class PrecoQtdViewSet(ModelViewSet):
    queryset = PrecoQuantidade.objects.all()
    serializer_class = PrecoQtdSerializer