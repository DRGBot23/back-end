from django.shortcuts import render, redirect
from pessoas.forms import LoginForm
from pessoas.models import Funcionario

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            funcionario = form.cleaned_data["funcionario"]
            request.session["funcionario_id"] = funcionario.id
            request.session["funcionario_tipo"] = funcionario.tipo
            return redirect("dashboard")
    else:
        form = LoginForm()

    return render(request, "pessoas/login.html", {"form": form})

def logout_view(request):
    request.session.flush()
    return redirect("login")
