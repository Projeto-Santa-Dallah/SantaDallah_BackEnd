from django.db import models
from .categoria import Categoria

class PrecoQuantidade(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="precosQtds", null=True, blank=True)
    quantidade = models.IntegerField(default=0) 
    preco = models.DecimalField(max_digits=7, decimal_places=2, default=0, null=True, blank=True)
    especial = models.BooleanField(blank=True, null=True)
    
    
    def __str__(self):
        preco_str = str(self.preco).replace(".", ",")
        especial_str = " - ESPECIAL" if self.especial else ""
        return f'{self.categoria.nome} - ({self.quantidade} unidades) - R${preco_str}{especial_str}'

    
    
    class Meta:
        verbose_name ="Preço Quantidade"
        verbose_name_plural = "Preço Quantidade"