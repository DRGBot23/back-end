from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from core.decorators import login_required, role_required
from .forms import ProdutoForm
from .models import Produto, Estoque


@login_required
def lista_produtos(request):
    produtos = Produto.objects.all().order_by("nome")
    return render(request, "produtos/produtos_lista.html", {"produtos": produtos})


@login_required
def estoque_baixo(request):
    produtos = Produto.objects.filter(
        estoque__quantidade__lte=models.F("minimo_estoque")
    ).order_by("estoque__quantidade")

    return render(request, "produtos/estoque_baixo.html", {
        "produtos": produtos
    })


@login_required
@role_required("ADM")
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect("lista_produtos")

    else:
        form = ProdutoForm(instance=produto)

    return render(request, "produtos/produto_form.html", {
        "form": form,
        "editar": True
    })


@login_required
@role_required("ADM")
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == "POST":
        produto.delete()
        return redirect("lista_produtos")

    return render(request, "produtos/confirmar_exclusao.html", {
        "objeto": produto
    })
