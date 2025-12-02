from django.urls import path
from .views import (
    lista_clientes, criar_cliente, editar_cliente, excluir_cliente,
    lista_funcionarios, criar_funcionario, editar_funcionario, excluir_funcionario
)

urlpatterns = [
    # Clientes
    path("clientes/", lista_clientes, name="lista_clientes"),
    path("clientes/novo/", criar_cliente, name="criar_cliente"),
    path("clientes/editar/<int:pk>/", editar_cliente, name="editar_cliente"),
    path("clientes/excluir/<int:pk>/", excluir_cliente, name="excluir_cliente"),

    # Funcionários
    path("funcionarios/", lista_funcionarios, name="lista_funcionarios"),
    path("funcionarios/novo/", criar_funcionario, name="criar_funcionario"),
    path("funcionarios/editar/<int:pk>/", editar_funcionario, name="editar_funcionario"),
    path("funcionarios/excluir/<int:pk>/", excluir_funcionario, name="excluir_funcionario"),
]
