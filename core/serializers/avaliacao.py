from rest_framework.serializers import ModelSerializer

from core.models import Avaliacao

class AvaliacaoListSerializer(ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ('id', 'comentario', 'nota')

class AvaliacaoRetriveSerializer(ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'
        depth = 1

class AvaliacaoSerializer(ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'
