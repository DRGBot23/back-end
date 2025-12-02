from django import forms
from django.forms import inlineformset_factory
from .models import Entrega, ItemEntrega
from produtos.models import Produto


class EntregaForm(forms.ModelForm):
    nota_fiscal = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional - será gerada se vazio'
        })
    )

    data_entrega = forms.DateField(
        required=True,
        input_formats=["%d/%m/%Y", "%Y-%m-%d"],
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'text'},
            format="%d/%m/%Y"
        )
    )

    class Meta:
        model = Entrega
        fields = ['nota_fiscal', 'data_entrega']


class ItemEntregaForm(forms.ModelForm):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        required=False,                    # <<--- AQUI!!!
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    produto_nome = forms.CharField(
        required=False,
        label="Nome do produto (se for novo)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Preencha se for novo produto'
        })
    )

    preco_compra = forms.DecimalField(
        required=False,
        label="Preço de compra",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    class Meta:
        model = ItemEntrega
        fields = ['produto', 'quantidade']

    def clean(self):
        cleaned = super().clean()
        produto = cleaned.get('produto')
        nome = cleaned.get('produto_nome')
        preco = cleaned.get('preco_compra')
        if not produto:
            if not nome:
                raise forms.ValidationError("Informe o nome do produto novo.")
            if not preco:
                raise forms.ValidationError("Informe o preço de compra do produto novo.")

        return cleaned



EntregaItemFormSet = inlineformset_factory(
    Entrega,
    ItemEntrega,
    form=ItemEntregaForm,
    extra=1,
    can_delete=False
)
