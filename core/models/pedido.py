from django.db import models
from django.core.exceptions import ValidationError

from .user import User
from .produto import Produto
from datetime import timedelta

class Pedido(models.Model):
    
    class FormaDeRetirada(models.IntegerChoices):
        RETIRADA = 1, 'Retirada'
        ENTREGA = 2, 'Entrega'
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, 'Carrinho'
        FINALIZADO = 2, 'Realizado'
        PAGO = 3, 'Pago'
        ENTREGUE = 4, 'Entregue'

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='compras')
    status = models.IntegerField(choices=StatusCompra.choices,  default=StatusCompra.CARRINHO)
    data_criacao = models.DateField(auto_now_add=True, blank=True, null=True)
    data_pedido = models.DateField (null=True, blank=True)
    horario_entrega = models.TimeField(null=True, blank=True)
    formaDeRetirada = models.IntegerField(choices=FormaDeRetirada.choices, default=FormaDeRetirada.ENTREGA)
    
 
    @property
    def total(self):
        # total = 0
        # for item in self.itens.all():
        #     total += item.livro.preco * item.quantidade
        # return total
        return sum(item.produto.preco * item.quantidade for item in self.itens.all())
    
   
 
class ItensPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='+')
    quantidade = models.IntegerField(default=1)