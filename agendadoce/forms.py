from django.forms import ModelForm
from django import forms
from .models import Entregador, Cliente, Pedido
from cliente.models import UsuarioAdaptado


class EntregadorForm(ModelForm):

    class Meta:
        model = Entregador
        fields = "__all__"
        widgets = {
            "nome_entregador": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "data_contratacao": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "veiculo": forms.TextInput(attrs={"class": "form-control"}),
            "disponibilidade": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class EntregadorFiltroForm(forms.Form):
    """Formulário para filtrar vagas"""

    descricao = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Buscar por nome..."}),
        label="Descrição",
    )

    data_inicio = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}), label="Data Início"
    )

    data_fim = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}), label="Data Fim"
    )

    disponibilidade = forms.ChoiceField(
        required=False,
        label="Status",
        choices=[
            ("", "Todos"),
            ("true", "Disponível"),
            ("false", "Indisponível"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = "__all__"
        widgets = {
            "nome_cliente": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
        }


class PedidoForm(ModelForm):

    class Meta:
        model = Pedido
        fields = [
            "nome_pedido",
            "tipo_massa",
            "recheio",
            "formato",
            "tamanho",
            "foto",
            "observacoes",
            "data_entrega",
            "endereco_pedido",
            "tipo_pagamento",
            "status",
        ]
        widgets = {
            "nome_pedido": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_massa": forms.Select(attrs={"class": "form-select"}),
            "recheio": forms.Select(attrs={"class": "form-select"}),
            "formato": forms.TextInput(attrs={"class": "form-control"}),
            "tamanho": forms.Select(attrs={"class": "form-select"}),
            "foto": forms.FileInput(attrs={"class": "form-control"}),
            "observacoes": forms.TextInput(attrs={"class": "form-control", "rows": 3}),
            "data_entrega": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "endereco_pedido": forms.TextInput(attrs={"class": "form-control", "rows": 2}),
            "tipo_pagamento": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class PedidoFiltroForm(forms.Form):
    """Formulário para filtrar vagas"""

    descricao = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Buscar por nome de pedido..."}),
        label="Nome do Pedido",
    )

    data_inicio = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}), label="Data Início"
    )

    data_fim = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}), label="Data Fim"
    )

    cliente = forms.ModelChoiceField(
        required=False,
        queryset=UsuarioAdaptado.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Cliente",
    )

    entregador = forms.ModelChoiceField(
        required=False,
        queryset=Entregador.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Entregador",
    )

    STATUS_CHOICES = [
        ("", "---------"),
        ("Aguardando Confirmação", "Aguardando Confirmação"),
        ("Em producao", "Em Produção"),
        ("Entregue", "Entregue"),
        ("Cancelado", "Cancelado"),
    ]

    status = forms.ChoiceField(
        required=False,
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Status do pedido",
    )
