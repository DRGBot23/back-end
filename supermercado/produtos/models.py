from django.db import models


class Produto(models.Model):
    codigo_barras = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=100)
    preco_compra = models.FloatField()
    preco_venda = models.FloatField()
    minimo_estoque = models.IntegerField(default=0)

    def __str__(self):
        return self.nome


class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    def abaixo_do_minimo(self):
        return self.quantidade < self.produto.minimo_estoque

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} unidades"

