from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

from .produto import Produto, ProdutoTamanho
from .tamanho import Tamanho
from .user import User
from .precoQtd import PrecoQuantidade


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
    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)
    data_criacao = models.DateField(auto_now_add=True, blank=True, null=True)
    data_pedido = models.DateField(null=True, blank=True)
    horario_entrega = models.TimeField(null=True, blank=True)
    formaDeRetirada = models.IntegerField(choices=FormaDeRetirada.choices, default=FormaDeRetirada.ENTREGA)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.email}"

    def total(self):
        return sum(item.total() for item in self.itens.all())


class ItensPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    produto_tamanho = models.ForeignKey(
        ProdutoTamanho, on_delete=models.PROTECT, null=True, blank=True
    )
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        if self.produto_tamanho:
            return f"{self.quantidade}x {self.produto.nome} ({self.produto_tamanho.tamanho.nome})"
        return f"{self.quantidade}x {self.produto.nome}"

    def total(self):
        """
        Calcula o total do item do pedido.
        - Se o produto for brigadeiro, usa a lógica de blocos (PrecoQuantidade).
        - Caso contrário, usa o preço do ProdutoTamanho.
        """
        if self.produto.categoria.filter(nome__iexact="Brigadeiro").exists():
            categorias = self.produto.categoria.all()
            precos_categoria = PrecoQuantidade.objects.filter(categoria__in=categorias)

            if not precos_categoria.exists():
                return 0

            quantidade = self.quantidade
            total = 0

         
            if quantidade < 25 or quantidade % 25 != 0:
               
                return 0

            precos_map = {pq.quantidade: pq.preco for pq in precos_categoria}

            restante = quantidade
            for bloco in sorted(precos_map.keys(), reverse=True):
                while restante >= bloco:
                    total += precos_map[bloco]
                    restante -= bloco

            return float(total)

      
        if self.produto_tamanho and hasattr(self.produto_tamanho, 'preco'):
            return float(self.produto_tamanho.preco) * self.quantidade

        return 0
