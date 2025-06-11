from rest_framework.serializers import ModelSerializer

from core.models import Orcamento

class OrcamentoListSerializer(ModelSerializer):
    class Meta:
        model = Orcamento
        fields = ('id', 'usuario', 'data', 'local')

class OrcamentoRetriveSerializer(ModelSerializer):
    class Meta:
        model = Orcamento
        fields = '__all__'
        depth = 1

class OrcamentoSerializer(ModelSerializer):
    class Meta:
        model = Orcamento
        fields = '__all__'
