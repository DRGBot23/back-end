from django import forms
from .models import Produto, Estoque

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['codigo_barras', 'nome', 'preco_compra', 'preco_venda', 'minimo_estoque']
        widgets = {
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'minimo_estoque': forms.NumberInput(attrs={'class': 'form-control'}),
        }
