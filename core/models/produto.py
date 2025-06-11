from django.db import models
from .categoria import Categoria
from .tamanho import Tamanho

class Produto(models.Model):
    class Tipo(models.IntegerChoices):
        NORMAL = 1, "Normal"
        ESPECIAL= 2, "Especial"
        PISTACHE = 3, "Pistache"
    nome = models.CharField(max_length=100)
    # categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='categorias', null=True, blank=True)
    categoria = models.ManyToManyField(Categoria, related_name="categorias", blank=True)
    descricao = models.CharField(max_length=400)
    tipo = models.IntegerField(choices=Tipo.choices,  default=Tipo.NORMAL)
    validade = models.IntegerField(default=0,blank=True, null=True)
    preco = models.DecimalField(max_digits=7, decimal_places=2, default=0, null=True, blank=True)
    sabor = models.CharField(max_length=100)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.PROTECT, related_name="tamanhos", null=True, blank=True)
    
    
    def __str__(self):
        categorias_nomes = ", ".join([cat.nome for cat in self.categoria.all()]) if self.pk else "Sem categoria"
        tamanho_nome = self.tamanho.nome if self.tamanho else "Sem tamanho"
        preco_str = str(self.preco).replace(".", ",") if self.preco else "0,00"
        return f'{self.nome} - {categorias_nomes} ({tamanho_nome}) - R${preco_str}'
