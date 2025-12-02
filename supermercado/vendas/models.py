from django.db import models
from produtos.models import Produto, Estoque
from pessoas.models import Funcionario, Cliente


class Venda(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    data_venda = models.DateField()
    valor_total = models.FloatField(default=0)

    def __str__(self):
        return f"Venda #{self.id} - {self.data_venda}"


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    @property
    def subtotal(self):
        return self.quantidade * float(self.produto.preco_venda)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        estoque, _ = Estoque.objects.get_or_create(produto=self.produto)
        estoque.quantidade -= self.quantidade
        estoque.save()
