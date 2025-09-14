from django.contrib import admin
from django.utils.html import format_html
from .models import Vendedor, Cliente, Pedido

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nome_vendedor', 'cpf', 'email', 'telefone', 'data_contratacao')
    fields = ('nome_vendedor', 'cpf', 'email', 'telefone', 'data_contratacao')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'cpf',  'email', 'telefone','endereco')
    fields = ('nome_cliente', 'cpf', 'email', 'telefone','endereco')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('nome_pedido', 'cliente', 'foto_thumbnail', 'data_entrega', 'status', 'valor')
    fields = ('nome_pedido', 'cliente', 'foto', 'tipo_massa', 'recheio', 'formato', 'tamanho', 'andares', 'observacoes', 'data_entrega', 'endereco_pedido', 'tipo_pagamento', 'status', 'valor')
    
    def foto_thumbnail(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.foto.url
            )
        return "Sem foto"
    foto_thumbnail.short_description = 'Foto'

