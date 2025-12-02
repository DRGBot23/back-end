from django import forms
from .models import Cliente, Funcionario, Endereco
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        senha = cleaned.get("senha")

        if email and senha:
            try:
                funcionario = Funcionario.objects.get(email=email)
            except Funcionario.DoesNotExist:
                raise forms.ValidationError("Email não encontrado.")

            if not check_password(senha, funcionario.senha):
                raise forms.ValidationError("Senha incorreta.")

            cleaned["funcionario"] = funcionario

        return cleaned


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'bairro', 'cidade', 'estado']
        widgets = {
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'data_nasc', 'email', 'fidelidade', 'pontos']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nasc': forms.DateInput(
                format='%d/%m/%Y',
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fidelidade': forms.CheckboxInput(),
            'pontos': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_nasc'].input_formats = ['%d/%m/%Y']


class FuncionarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'data_nasc', 'email', 'senha', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nasc': forms.DateInput(
                format='%d/%m/%Y',
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_nasc'].input_formats = ['%d/%m/%Y']

    def clean_senha(self):
        raw = self.cleaned_data['senha']
        return make_password(raw)
