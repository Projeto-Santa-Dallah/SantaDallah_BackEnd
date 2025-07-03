from django.db import models

class Endereco (models.Model):
    ESTADOS = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]
     
    cep = models.CharField(max_length=8)
    estado = models.CharField(max_length=2, choices=ESTADOS)
    cidade = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100, blank=True)
    logradouro = models.CharField(max_length=100, blank=True)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=150, blank=True, null=True)
    
    
    def __str__(self):
        return f'{self.bairro} - {self.logradouro} - {self.numero}'
    
    class Meta:
        verbose_name ="Endereço"
        verbose_name_plural = "Endereços"
    