from rest_framework.serializers import ModelSerializer

from core.models import Tamanho

class TamanhoListSerializer(ModelSerializer):
    class Meta:
        model = Tamanho
        fields = ("id", "nome", "qtdFatia", "formato")

class TamanhoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Tamanho
        fields = "__all__"
        depth = 1

class TamanhoSerializer(ModelSerializer):
    class Meta:
        model = Tamanho
        fields = "__all__"