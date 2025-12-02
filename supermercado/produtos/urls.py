from django.urls import path
from .views import (
    lista_produtos,
    estoque_baixo,
    editar_produto,
    excluir_produto,
)

urlpatterns = [
    path("lista/", lista_produtos, name="lista_produtos"),
    path("estoque-baixo/", estoque_baixo, name="estoque_baixo"),
    path("editar/<int:pk>/", editar_produto, name="editar_produto"),
    path("excluir/<int:pk>/", excluir_produto, name="excluir_produto"),
]
