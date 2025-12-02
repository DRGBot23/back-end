from django.db import models
from django.contrib.auth.models import AbstractUser


class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro}"


class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    data_nasc = models.DateField()
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Cliente(Pessoa):
    pontos = models.IntegerField(default=0)
    fidelidade = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Funcionario(Pessoa):
    TIPO = (
        ('ADM', 'Administrador'),
        ('FUNC', 'Funcionário'),
    )
    tipo = models.CharField(max_length=4, choices=TIPO)

    def __str__(self):
        return f"{self.nome} - {self.get_tipo_display()}"


