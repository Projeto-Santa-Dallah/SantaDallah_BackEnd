from django.db import models
from .user import User
from uploader.models import Image

class Orcamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orcamentos", null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    qtnPessoas = models.IntegerField(default=0,null=True, blank=True)
    local = models.CharField(max_length=10,null=True, blank=True)
    bebidaAlcoolica = models.BooleanField(null=True, blank=True)
    docinhos = models.BooleanField(null=True, blank=True)
    foto = models.ManyToManyField(
        Image,
        related_name="orcamento_foto",
        blank=True,
        default=None,
    )
    
    def __str__(self):
        return f'{self.usuario} ({self.data})'