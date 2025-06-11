from django.db import models
from .user import User

class Orcamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orcamentos", null=True, blank=True)
    data = models.DateField(null=False)
    qtnPessoas = models.IntegerField(default=0)
    local = models.CharField(max_length=100)
    consideracoes = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.usuario} ({self.data})'