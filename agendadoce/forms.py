from django.forms import ModelForm
from django import forms
from .models import Vendedor, Cliente, Pedido

class VendedorForm(ModelForm):

    class Meta:
        model = Vendedor
        fields = '__all__'
        widgets = {
            'nome_vendedor': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nome_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class PedidoForm(ModelForm):

    class Meta:
        model = Pedido
        fields = {'nome_pedido', 'cliente', 'tipo_massa', 'recheio', 'formato', 'tamanho', 'andares', 'imagem', 'observacoes', 'data_entrega', 'endereco_pedido', 'tipo_pagamento', 'imagem_thumbnail'} 
        widgets = {
            'nome_pedido': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control' }),
            'tipo_massa': forms.SelectInput(attrs={'class': 'form-control' }),
            'recheio': forms.SelectInput(attrs={'class': 'form-control' }),
            'formato': forms.TextInput(attrs={'class': 'form-control' }),
            'tamanho': forms.Select(attrs={'class': 'form-control' }),
            'andares': forms.Select(attrs={'class': 'form-control' }),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            'observacoes': forms.TextInput(attrs={'class': 'form-control' }),
            'data_entrega': forms.DateTimeInput(attrs={'class': 'form-control' }),
            'endereco_pedido': forms.TextInput(attrs={'class': 'form-control' }),
            'tipo_pagamento': forms.Select(attrs={'class': 'form-control' }),
        }