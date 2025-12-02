from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import transaction
from core.decorators import login_required, role_required
from .forms import VendaForm, ItemVendaFormSet
from .models import Venda, ItemVenda
from pessoas.models import Funcionario
from produtos.models import Produto, Estoque


@login_required
def lista_vendas(request):
    vendas = Venda.objects.all().order_by("-data_venda")
    funcionario_tipo = request.session.get("funcionario_tipo")

    return render(request, "vendas/lista_vendas.html", {
        "vendas": vendas,
        "funcionario_tipo": funcionario_tipo
    })


@login_required
def nova_venda(request):
    if request.session.get("funcionario_tipo") != "FUNC":
        return render(request, "erro.html", {
            "mensagem": "Apenas funcionários podem registrar vendas."
        })

    funcionario = Funcionario.objects.get(
        pk=request.session.get("funcionario_id")
    )

    if request.method == "POST":
        form = VendaForm(request.POST)
        formset = ItemVendaFormSet(request.POST, prefix="itens")

        if form.is_valid() and formset.is_valid():

            with transaction.atomic():

                venda = form.save(commit=False)
                venda.funcionario = funcionario
                venda.valor_total = 0
                venda.save()

                total_final = 0
                total_forms = int(request.POST.get("itens-TOTAL_FORMS", 0))

                for i in range(total_forms):

                    produto_id = request.POST.get(f"itens-{i}-produto")
                    quantidade = request.POST.get(f"itens-{i}-quantidade")

                    if not produto_id or not quantidade:
                        continue

                    produto = Produto.objects.filter(id=produto_id).first()
                    if not produto:
                        continue

                    quantidade = int(quantidade)

                    item = ItemVenda.objects.create(
                        venda=venda,
                        produto=produto,
                        quantidade=quantidade
                    )

                    total_final += item.subtotal

                    estoque, _ = Estoque.objects.get_or_create(produto=produto)
                    estoque.quantidade -= quantidade
                    estoque.save()

                venda.valor_total = total_final
                venda.save()

            return redirect("lista_vendas")

    else:
        form = VendaForm(initial={"data_venda": timezone.now().date()})
        formset = ItemVendaFormSet(prefix="itens")

    produtos = Produto.objects.all()

    return render(request, "vendas/nova_venda.html", {
        "form": form,
        "formset": formset,
        "produto_list": produtos
    })


@login_required
def detalhe_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    itens = ItemVenda.objects.filter(venda=venda)

    return render(request, "vendas/detalhe_venda.html", {
        "venda": venda,
        "itens": itens
    })

@login_required
@role_required("ADM")
def excluir_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)

    if request.method == "POST":
        venda.delete()
        return redirect("lista_vendas")

    return render(request, "vendas/confirmar_exclusao_venda.html", {
        "objeto": venda
    })

