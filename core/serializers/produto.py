from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from uploader.models import Image
from uploader.serializers import ImageSerializer
from core.models import Produto, Categoria, Tamanho, PrecoQuantidade, ProdutoTamanho


class ProdutoTamanhoSerializer(serializers.ModelSerializer):
    tamanho_nome = serializers.CharField(source="tamanho.nome", read_only=True)
    preco = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)

    class Meta:
        model = ProdutoTamanho
        fields = ["id", "tamanho_nome", "preco"]


class ProdutoListSerializer(ModelSerializer):
    foto_url = serializers.SerializerMethodField()
    preco = serializers.SerializerMethodField()
    tamanhos = ProdutoTamanhoSerializer(source="produto_tamanho", many=True, read_only=True)

    class Meta:
        model = Produto
        fields = ["id", "nome", "sabor", "tamanhos", "foto_url", "preco"]

    def get_foto_url(self, obj):
        if obj.foto.exists():
            return obj.foto.first().url
        return None

    def get_preco(self, obj):
        """
        Retorna o preço do produto:
        - Se tiver tamanhos, retorna None (os preços estão em 'tamanhos').
        - Se for brigadeiro, calcula com base na quantidade.
        """
 
        if obj.tamanhos.exists():
            return None

        request = self.context.get("request")
        quantidade = request.query_params.get("quantidade")
        categorias = obj.categoria.all()


        if not obj.categoria.filter(nome__iexact="Brigadeiro").exists():
            return 0

  
        if not quantidade:
    
            precos_categoria = PrecoQuantidade.objects.filter(categoria__in=categorias)
            if precos_categoria.exists():
                return float(precos_categoria.order_by("quantidade").first().preco)
            return 0

        try:
            quantidade = int(quantidade)
        except ValueError:
            raise serializers.ValidationError({"quantidade": "Deve ser um número inteiro."})

        if quantidade < 25:
            raise serializers.ValidationError({"quantidade": "O pedido mínimo é 25 brigadeiros."})
        if quantidade % 25 != 0:
            raise serializers.ValidationError({"quantidade": "A quantidade deve ser múltipla de 25."})

    
        precos_categoria = PrecoQuantidade.objects.filter(categoria__in=categorias)
        precos_map = {pq.quantidade: pq.preco for pq in precos_categoria}

        total = 0
        restante = quantidade
        for bloco in sorted(precos_map.keys(), reverse=True):
            while restante >= bloco:
                total += precos_map[bloco]
                restante -= bloco

        return round(total, 2)


class ProdutoRetrieveSerializer(ModelSerializer):
    foto = ImageSerializer(many=True, required=False)
    tamanhos = ProdutoTamanhoSerializer(source="produto_tamanho", many=True, read_only=True)


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
    tamanhos = ProdutoTamanhoSerializer(source="produto_tamanho", many=True, read_only=True)


    class Meta:
        model = Produto
        fields = "__all__"

    def validate(self, data):

        instance = getattr(self, "instance", None)

      
        tamanhos_existentes = instance.tamanhos.exists() if instance else False
        tamanhos_novos = data.get("tamanhos", None)
        has_tamanhos = tamanhos_existentes or (
            tamanhos_novos is not None and len(tamanhos_novos) > 0
        )

        if has_tamanhos and data.get("preco"):
            raise serializers.ValidationError(
                "Produtos com tamanhos não devem ter preço direto."
            )
        if not has_tamanhos and not data.get("preco"):
            raise serializers.ValidationError(
                "Produtos sem tamanhos precisam ter preço direto."
            )

        return data
