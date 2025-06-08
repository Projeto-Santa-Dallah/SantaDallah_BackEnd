from django.db import models
from .categoria import Categoria

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='categorias', null=True, blank=True)
    descricao = models.CharField(max_length=400)
    validade = models.IntegerField(default=0,blank=True, null=True)
    especial = models.BooleanField(default=False)
    preco = models.DecimalField(max_digits=7, decimal_places=2, default=0, null=True, blank=True)
    tamanho = models.DecimalField(max_digits=4, decimal_places=2, default=0, null=True, blank=True)
    sabor = models.CharField(max_length=100)
    
    
    def __str__(self):
        return f'{self.nome} ({self.categoria.nome})'