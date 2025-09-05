from django.db import models
from .user import User

class Orcamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orcamentos", null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    qtnPessoas = models.IntegerField(default=0,null=True, blank=True)
    local = models.CharField(max_length=10,null=True, blank=True)
    bebidaAlcoolica = models.BooleanField(null=True, blank=True)
    docinhos = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.usuario} ({self.data})'