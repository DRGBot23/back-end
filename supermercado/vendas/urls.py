from django.urls import path
from .views import lista_vendas, nova_venda, detalhe_venda, excluir_venda

urlpatterns = [
    path("", lista_vendas, name="lista_vendas"),
    path("nova/", nova_venda, name="nova_venda"),
    path("<int:pk>/", detalhe_venda, name="detalhe_venda"),
    path("<int:pk>/excluir/", excluir_venda, name="excluir_venda"),
]
