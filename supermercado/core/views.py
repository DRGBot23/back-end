from django.shortcuts import render
from django.utils import timezone
from core.decorators import login_required
from vendas.models import Venda
from entregas.models import Entrega
from pessoas.models import Cliente
from produtos.models import Produto
from django.db import models
from django.db.models import Sum


@login_required
def dashboard(request):

    hoje = timezone.now().date()

    vendas_hoje = Venda.objects.filter(data_venda=hoje)
    entregas_hoje = Entrega.objects.filter(data_entrega=hoje)
    clientes_total = Cliente.objects.count()

    produtos_baixo = Produto.objects.filter(
        estoque__quantidade__lte=models.F("minimo_estoque")
    )

    contexto = {
        "vendas_hoje": vendas_hoje,
        "total_vendas": vendas_hoje.count(),
        "total_vendas_valor": vendas_hoje.aggregate(total=Sum("valor_total"))["total"] or 0,

        "entregas_hoje": entregas_hoje,
        "total_entregas": entregas_hoje.count(),
        "total_entregas_valor": entregas_hoje.aggregate(total=Sum("valor_total"))["total"] or 0,

        "clientes_total": clientes_total,
        "produtos_baixo": produtos_baixo,
    }

    return render(request, "dashboard.html", contexto)
