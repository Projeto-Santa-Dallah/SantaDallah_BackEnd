from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from uploader.models import Image
from uploader.serializers import ImageSerializer
from core.models import Produto, Categoria, Tamanho


class ProdutoListSerializer(ModelSerializer):
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = ("id", "nome", "preco", "sabor", "foto_url")

    def get_foto_url(self, obj):
        if obj.foto.exists():
            return obj.foto.first().url  # Ou o campo que tem a url da imagem
        return None


class ProdutoRetrieveSerializer(ModelSerializer):
    foto = ImageSerializer(many=True, required=False)  
    class Meta:
        model = Produto
        fields = "__all__"
        depth = 1


class ProdutoSerializer(ModelSerializer):
    foto_attachment_keys = SlugRelatedField(
        source='foto',  
        many=True,
        queryset=Image.objects.all(),
        slug_field='attachment_key',
        required=False,
        write_only=True,
    )
    foto = ImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Produto
        fields = "__all__"
