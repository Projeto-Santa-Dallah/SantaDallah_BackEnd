from rest_framework.serializers import ModelSerializer

from core.models import PrecoQuantidade


class PrecoQtdListSerializer(ModelSerializer):
    class Meta:
        model = PrecoQuantidade
        fields = ("id", "categoria", "quantidade", "preco")


class PrecoQtdRetrieveSerializer(ModelSerializer):
    class Meta:
        model = PrecoQuantidade
        fields = "__all__"
        depth = 1  


class PrecoQtdSerializer(ModelSerializer):
    class Meta:
        model = PrecoQuantidade
        fields = "__all__"
