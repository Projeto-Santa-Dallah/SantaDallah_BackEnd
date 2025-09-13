from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField,  CurrentUserDefault,  HiddenField
from core.models import Pedido, ItensPedido

class ItensPedidoSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.produto.preco * instance.quantidade

    
    class Meta:
        model = ItensPedido
        fields = ('produto', 'quantidade', 'total')
        depth = 1

class PedidoSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    itens = ItensPedidoSerializer(many=True, read_only=True)
    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'status', 'total', 'itens')
        
class ItensPedidoCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensPedido
        fields = ('produto', 'quantidade')
        
class PedidoCreateUpdateSerializer(ModelSerializer):
    itens = ItensPedidoCreateUpdateSerializer(many=True)
    usuario = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Pedido
        fields = ('usuario', 'itens')
        
        
    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        for item_data in itens_data:
            ItensPedido.objects.create(pedido=pedido, **item_data)
        pedido.save()
        return pedido
    
    def update(self, pedido, validated_data):
        itens_data = validated_data.pop('itens', [])
        if itens_data:
            pedido.itens.all().delete()
            for item_data in itens_data:
                ItensPedido.objects.create(pedido=pedido, **item_data)
        return super().update(pedido, validated_data)
    
class ItensPedidoListSerializer(ModelSerializer):
    produto= CharField(source='produto.nome', read_only=True)

    class Meta:
        model = ItensPedido
        fields = ('quantidade', 'produto')
        depth = 1
    
class PedidoListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensPedidoListSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'itens')