from rest_framework.serializers import ModelSerializer

from core.models import PrecoQuantidade

class PrecoQtdSerializer(ModelSerializer):
    class Meta:
        model = PrecoQuantidade
        fields = "__all__"
        depth = 1