from rest_framework.viewsets import ModelViewSet

from core.models import Orcamento
from core.serializers import OrcamentoSerializer

class OrcamentoViewSet(ModelViewSet):
    queryset = Orcamento.objects.all()
    serializer_class = OrcamentoSerializer