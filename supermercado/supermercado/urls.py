from django.contrib import admin
from django.urls import path, include
from core.views import dashboard
from pessoas.views_auth import login_view, logout_view


urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    #Rotas dos Apps
    path('produtos/', include('produtos.urls')),
    path('entregas/', include('entregas.urls')),
    path('vendas/', include('vendas.urls')),
    path('pessoas/', include('pessoas.urls')),
]
