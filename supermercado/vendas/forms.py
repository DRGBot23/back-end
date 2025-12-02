from django import forms
from django.forms import inlineformset_factory
from .models import Venda, ItemVenda
from pessoas.models import Cliente


class VendaForm(forms.ModelForm):

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=True,
        label="Cliente",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Venda
        fields = ["data_venda", "cliente"]

        widgets = {
            "data_venda": forms.DateInput(
                format="%d/%m/%Y",
                attrs={
                    "class": "form-control",
                    "placeholder": "dd/mm/aaaa"
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["data_venda"].input_formats = ["%d/%m/%Y"]


class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ["produto", "quantidade"]
        widgets = {
            "produto": forms.Select(attrs={"class": "form-control produto-select"}),
            "quantidade": forms.NumberInput(
                attrs={"class": "form-control quantidade-input", "min": "1"}
            ),
        }


ItemVendaFormSet = inlineformset_factory(
    Venda,
    ItemVenda,
    form=ItemVendaForm,
    extra=1,
    can_delete=True
)
