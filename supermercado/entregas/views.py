from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.utils import timezone
from core.decorators import login_required, role_required
from .forms import EntregaForm, EntregaItemFormSet
from .models import Entrega, ItemEntrega
from produtos.models import Produto, Estoque
from decimal import Decimal
import random


@login_required
def lista_entregas(request):
    entregas = Entrega.objects.all().order_by("-data_entrega")
    return render(request, "entregas/lista_entregas.html", {"entregas": entregas})


@login_required
def detalhes_entrega(request, pk):
    entrega = get_object_or_404(Entrega, pk=pk)
    itens = entrega.itementrega_set.all()

    return render(request, "entregas/detalhes_entrega.html", {
        "entrega": entrega,
        "itens": itens
    })


@login_required
@role_required("ADM")
def criar_entrega(request):

    produtos = Produto.objects.all()

    if request.method == "POST":
        form = EntregaForm(request.POST)
        formset = EntregaItemFormSet(request.POST, prefix="itens")

        print("\nVALIDAÇÃO ENTREGA:", form.is_valid())
        print("Erros:", form.errors)
        print("VALIDAÇÃO ITENS:", formset.is_valid())
        print("Erros itens:", formset.errors)

        if form.is_valid() and formset.is_valid():

            with transaction.atomic():

                entrega = form.save(commit=False)

                if not entrega.nota_fiscal:
                    entrega.nota_fiscal = str(random.randint(10**7, 10**8 - 1))

                entrega.valor_total = Decimal("0.00")
                entrega.save()

                for item_form in formset:

                    cd = item_form.cleaned_data
                    if not cd:
                        continue

                    produto = cd.get("produto")
                    nome_novo = cd.get("produto_nome")
                    preco_compra = cd.get("preco_compra")
                    quantidade = cd.get("quantidade")

                    if not produto and nome_novo:
                        preco_compra = Decimal(str(preco_compra))
                        preco_venda = (preco_compra + Decimal("2.00")).quantize(Decimal("0.01"))
                        from random import randint
                        while True:
                            codigo = str(randint(10**12, 10**13 - 1)) 
                            if not Produto.objects.filter(codigo_barras=codigo).exists():
                                break

                        produto = Produto.objects.create(
                            nome=nome_novo,
                            preco_compra=preco_compra,
                            preco_venda=preco_venda,
                            minimo_estoque=10,
                            codigo_barras=codigo 
                        )

                        Estoque.objects.create(produto=produto, quantidade=0)

                    item = ItemEntrega(
                        entrega=entrega,
                        produto=produto,
                        quantidade=quantidade
                    )
                    item.save()

                    estoque, _ = Estoque.objects.get_or_create(produto=produto)
                    estoque.quantidade += quantidade
                    estoque.save()

                    if preco_compra not in (None, ""):
                        valor_item = Decimal(str(preco_compra)) * Decimal(str(quantidade))
                    else:
                        valor_item = Decimal(str(produto.preco_compra)) * Decimal(str(quantidade))

                    entrega.valor_total += valor_item

                entrega.save()

            return redirect("lista_entregas")

        else:
            print("\n>>> FORM ou FORMSET INVÁLIDO — NÃO SALVOU <<<")

    else:
        form = EntregaForm(initial={
            "data_entrega": timezone.now().strftime("%d/%m/%Y")
        })
        formset = EntregaItemFormSet(prefix="itens")

    return render(request, "entregas/entrega_form.html", {
        "form": form,
        "formset": formset,
        "produtos": produtos,
    })

@login_required
@role_required("ADM")
def excluir_entrega(request, pk):
    entrega = get_object_or_404(Entrega, pk=pk)

    if request.method == "POST":
        entrega.delete()
        return redirect("lista_entregas")

    return render(request, "entregas/confirmar_exclusao_entrega.html", {
        "objeto": entrega
    })

