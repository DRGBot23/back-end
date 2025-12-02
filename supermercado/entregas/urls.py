from django.urls import path
from .views import lista_entregas, criar_entrega, detalhes_entrega, excluir_entrega

urlpatterns = [
    path('', lista_entregas, name='lista_entregas'),
    path('nova/', criar_entrega, name='nova_entrega'),
    path('<int:pk>/', detalhes_entrega, name='detalhes_entrega'),
    path('<int:pk>/excluir/', excluir_entrega, name='excluir_entrega'),
]
