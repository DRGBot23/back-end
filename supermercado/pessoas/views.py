from django.shortcuts import render, redirect, get_object_or_404
from core.decorators import login_required, role_required
from .forms import ClienteForm, FuncionarioForm, EnderecoForm
from .models import Cliente, Funcionario


@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "pessoas/lista_clientes.html", {"clientes": clientes})


@login_required
def criar_cliente(request):
    if request.method == "POST":
        form_cliente = ClienteForm(request.POST)
        form_endereco = EnderecoForm(request.POST)

        if form_cliente.is_valid() and form_endereco.is_valid():
            end = form_endereco.save()
            cli = form_cliente.save(commit=False)
            cli.endereco = end
            cli.save()
            return redirect("lista_clientes")

    else:
        form_cliente = ClienteForm()
        form_endereco = EnderecoForm()

    return render(request, "pessoas/cliente_form.html", {
        "form_cliente": form_cliente,
        "form_endereco": form_endereco
    })


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    endereco = cliente.endereco

    if request.method == "POST":
        form_cliente = ClienteForm(request.POST, instance=cliente)
        form_endereco = EnderecoForm(request.POST, instance=endereco)

        if form_cliente.is_valid() and form_endereco.is_valid():
            form_endereco.save()
            form_cliente.save()
            return redirect("lista_clientes")

    else:
        form_cliente = ClienteForm(instance=cliente)
        form_endereco = EnderecoForm(instance=endereco)

    return render(request, "pessoas/cliente_form.html", {
        "form_cliente": form_cliente,
        "form_endereco": form_endereco,
        "editar": True
    })


@login_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        cliente.endereco.delete()
        cliente.delete()
        return redirect("lista_clientes")

    return render(request, "pessoas/confirmar_exclusao_cliente.html", {
        "objeto": cliente
    })


@login_required
@role_required("ADM")
def lista_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, "pessoas/lista_funcionarios.html", {"funcionarios": funcionarios})


@login_required
@role_required("ADM")
def criar_funcionario(request):
    if request.method == "POST":
        form_func = FuncionarioForm(request.POST)
        form_end = EnderecoForm(request.POST)
        if form_func.is_valid() and form_end.is_valid():
            end = form_end.save()
            func = form_func.save(commit=False)
            func.endereco = end
            func.save()
            return redirect("lista_funcionarios")

    else:
        form_func = FuncionarioForm()
        form_end = EnderecoForm()

    return render(request, "pessoas/funcionario_form.html", {
        "form_funcionario": form_func,
        "form_endereco": form_end
    })


@login_required
@role_required("ADM")
def editar_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    endereco = funcionario.endereco

    if request.method == "POST":
        form_funcionario = FuncionarioForm(request.POST, instance=funcionario)
        form_endereco = EnderecoForm(request.POST, instance=endereco)

        if form_funcionario.is_valid() and form_endereco.is_valid():
            form_endereco.save()

            from django.contrib.auth.hashers import make_password
            func = form_funcionario.save(commit=False)
            func.senha = make_password(form_funcionario.cleaned_data["senha"])
            func.save()

            return redirect("lista_funcionarios")

    else:
        form_funcionario = FuncionarioForm(instance=funcionario)
        form_endereco = EnderecoForm(instance=endereco)

    return render(request, "pessoas/funcionario_form.html", {
        "form_funcionario": form_funcionario,
        "form_endereco": form_endereco,
        "editar": True
    })


@login_required
@role_required("ADM")
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)

    if request.method == "POST":
        funcionario.endereco.delete()
        funcionario.delete()
        return redirect("lista_funcionarios")

    return render(request, "pessoas/confirmar_exclusao_funcionario.html", {
        "objeto": funcionario
    })
