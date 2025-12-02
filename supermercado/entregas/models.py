from django.db import models
from produtos.models import Produto


class Entrega(models.Model):
    nota_fiscal = models.CharField(max_length=30)
    data_entrega = models.DateField()
    valor_total = models.FloatField()

    def __str__(self):
        return f"Entrega NF {self.nota_fiscal}"


class ItemEntrega(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
