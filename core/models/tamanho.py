from django.db import models 
from .categoria import Categoria

class Tamanho(models.Model):
   

    nome = models.CharField(max_length=10)
    qtdFatia = models.IntegerField(default=0)
    massakg = models.DecimalField(max_digits=4, decimal_places=2, default=0, null=True, blank=True)
    # preco = models.DecimalField(max_digits=7, decimal_places=2, default=0, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='tamanhos',null=True, blank=True)
    formato = models.CharField(max_length=50)
   
    
    
    def __str__(self):
        return f'{self.nome.upper()} - ({self.categoria.nome}) - ({self.qtdFatia} fatias)'