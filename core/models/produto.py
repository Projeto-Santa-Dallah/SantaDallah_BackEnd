from django.db import models
from .categoria import Categoria
from .tamanho import Tamanho
from uploader.models import Image


class Produto(models.Model):
    class Tipo(models.IntegerChoices):
        NORMAL = 1, "Normal"
        ESPECIAL = 2, "Especial"
        PISTACHE = 3, "Pistache"

    nome = models.CharField(max_length=100)
    categoria = models.ManyToManyField(Categoria, related_name="produtos", blank=True)
    descricao = models.CharField(max_length=400)
    tipo = models.IntegerField(choices=Tipo.choices, default=Tipo.NORMAL)
    validade = models.IntegerField(default=0, blank=True, null=True)
    # preco = models.DecimalField(max_digits=7, decimal_places=2, default=0, null=True, blank=True)
    sabor = models.CharField(max_length=100)
    tamanhos = models.ManyToManyField(Tamanho, through='ProdutoTamanho', related_name='produtos', blank=True)
    foto = models.ManyToManyField(
        Image,
        related_name="produto_foto",
        blank=True,
        default=None,
    )

    def __str__(self):
        categorias_nomes = ", ".join([cat.nome for cat in self.categoria.all()]) if self.pk else "Sem categoria"
        # preco_str = str(self.preco).replace(".", ",") if self.preco else "0,00"
        return f'{self.nome} - {categorias_nomes}'


class ProdutoTamanho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        unique_together = ('produto', 'tamanho')

    def __str__(self):
        return f"{self.produto.nome} - {self.tamanho.nome} - R${self.preco}"
