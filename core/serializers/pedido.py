from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField, HiddenField, CurrentUserDefault, DateField, TimeField
from core.models import Pedido, ItensPedido, Produto, ProdutoTamanho, PrecoQuantidade
from django.utils import timezone
from datetime import timedelta


class ItensPedidoSerializer(ModelSerializer):
    total = SerializerMethodField()
    produto_nome = CharField(source='produto.nome', read_only=True)
    tamanho_nome = SerializerMethodField()

    class Meta:
        model = ItensPedido
        fields = ('produto', 'produto_nome', 'produto_tamanho', 'tamanho_nome', 'quantidade', 'total')
        depth = 1

    def get_total(self, instance):
        return instance.total()

    def get_tamanho_nome(self, instance):
        return instance.produto_tamanho.tamanho.nome if instance.produto_tamanho else None


class PedidoSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    itens = ItensPedidoSerializer(many=True, read_only=True)
    total = SerializerMethodField()
    data_pedido = DateField(read_only=True)
    data_criacao = DateField(read_only=True)
    horario_entrega = TimeField(read_only=True)

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'status', 'total', 'itens', 'data_pedido', 'data_criacao', 'horario_entrega')

    def get_total(self, obj):
        return sum(item.total() for item in obj.itens.all())


class ItensPedidoCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensPedido
        fields = ('produto', 'produto_tamanho', 'quantidade')


class PedidoCreateUpdateSerializer(ModelSerializer):
    itens = ItensPedidoCreateUpdateSerializer(many=True)
    usuario = HiddenField(default=CurrentUserDefault())
    data_pedido = DateField()

    class Meta:
        model = Pedido
        fields = ('usuario', 'itens', 'data_pedido')

    def validate(self, attrs):
        data_pedido = attrs.get('data_pedido')
        data_criacao = timezone.now().date()
        if (data_pedido - data_criacao) <= timedelta(days=2):
            raise serializers.ValidationError("O pedido deve ser feito com 2 dias de antecedência.")
        return attrs

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)

        for item_data in itens_data:
            ItensPedido.objects.create(
                pedido=pedido,
                produto=item_data['produto'],
                produto_tamanho=item_data.get('produto_tamanho', None),
                quantidade=item_data['quantidade']
            )
        return pedido

    def update(self, instance, validated_data):
        itens_data = validated_data.pop('itens', [])
        if itens_data:
            instance.itens.all().delete()
            for item_data in itens_data:
                ItensPedido.objects.create(
                    pedido=instance,
                    produto=item_data['produto'],
                    produto_tamanho=item_data.get('produto_tamanho', None),
                    quantidade=item_data['quantidade']
                )
        return super().update(instance, validated_data)



class ItensPedidoListSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    tamanho_nome = serializers.SerializerMethodField()

    class Meta:
        model = ItensPedido
        fields = (
            'id',
            'produto',
            'produto_nome',
            'produto_tamanho',
            'tamanho_nome',
            'quantidade',
        )

    def get_tamanho_nome(self, instance):
        return instance.produto_tamanho.tamanho.nome if instance.produto_tamanho else None
    
class PedidoListSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source='usuario.email', read_only=True)
    itens = ItensPedidoListSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'itens', 'total')

    def get_total(self, obj):
        return sum(item.total() for item in obj.itens.all())