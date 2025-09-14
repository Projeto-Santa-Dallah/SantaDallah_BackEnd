from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField,  CurrentUserDefault,  HiddenField, DateField, TimeField
from core.models import Pedido, ItensPedido
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone


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
    data_pedido = DateField(read_only=True)
    data_criacao = DateField(read_only= True)
    itens = ItensPedidoSerializer(many=True, read_only=True)
    horario_entrega = TimeField(read_only= True)
    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'status', 'total', 'itens', 'data_pedido', 'data_criacao', 'horario_entrega')
        
        
        
        
class ItensPedidoCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensPedido
        fields = ('produto', 'quantidade')
        
class PedidoCreateUpdateSerializer(ModelSerializer):
    itens = ItensPedidoCreateUpdateSerializer(many=True)
    usuario = HiddenField(default=CurrentUserDefault())
    data_pedido = DateField()

    class Meta:
        model = Pedido
        fields = ('usuario', 'itens', 'data_pedido')
        
    def validate(self, attrs):
        data_pedido = attrs.get('data_pedido')
        data_criacao = timezone.now().date()  # Or pedido.data_criacao if updating
        if (data_pedido - data_criacao) <= timedelta(days=2):
            raise ValidationError("O pedido deve ser feito com 2 dias de antecedencia.")
        return attrs
       
        
        
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