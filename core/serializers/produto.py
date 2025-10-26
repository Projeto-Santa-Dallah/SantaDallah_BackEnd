from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from uploader.models import Image
from uploader.serializers import ImageSerializer
from core.models import Produto, Categoria, Tamanho, PrecoQuantidade


class ProdutoListSerializer(ModelSerializer):
    foto_url = serializers.SerializerMethodField()
    preco = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = ("id", "nome", "preco", "sabor", "foto_url", "preco")

    def get_foto_url(self, obj):
        if obj.foto.exists():
            return obj.foto.first().url  
        return None

    def get_preco(self, obj):
        request = self.context.get("request")
        quantidade = request.query_params.get("quantidade")

     
        is_brigadeiro = obj.categoria.filter(nome__iexact="Brigadeiro").exists()
        if not is_brigadeiro:
            return obj.preco 

        if not quantidade:
            categorias = obj.categoria.all()
            precos_categoria = PrecoQuantidade.objects.filter(categoria__in=categorias)
            if precos_categoria.exists():
                return float(precos_categoria.order_by('quantidade').first().preco)
            return obj.preco or 0

        try:
            quantidade = int(quantidade)
        except ValueError:
            raise serializers.ValidationError({"quantidade": "Deve ser um número inteiro."})

        if quantidade < 25:
            raise serializers.ValidationError({"quantidade": "O pedido mínimo é 25 brigadeiros."})

        if quantidade % 25 != 0:
            raise serializers.ValidationError({"quantidade": "A quantidade deve ser múltipla de 25 (25,50,75,100...)."})


        categorias = obj.categoria.all()
        precos_categoria = PrecoQuantidade.objects.filter(categoria__in=categorias)

        precos_map = {pq.quantidade: pq.preco for pq in precos_categoria if pq.quantidade in [25,50,100]}

        for base in [25,50,100]:
            if base not in precos_map:
                raise serializers.ValidationError({f"preco_{base}": f"Não há preço cadastrado para {base} brigadeiros."})

        total = 0
        restante = quantidade
        for bloco in [100,50,25]:
            while restante >= bloco:
                total += precos_map[bloco]
                restante -= bloco

        return round(total, 2)


class ProdutoRetrieveSerializer(ModelSerializer):
    foto = ImageSerializer(many=True, required=False)

    class Meta:
        model = Produto
        fields = "__all__"
        depth = 1


class ProdutoSerializer(ModelSerializer):
    foto_attachment_keys = SlugRelatedField(
        source="foto",
        many=True,
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
        write_only=True,
    )
    foto = ImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Produto
        fields = "__all__"
