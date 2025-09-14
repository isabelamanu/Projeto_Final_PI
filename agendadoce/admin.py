from django.contrib import admin
from django.utils.html import format_html
from .models import Vendedor, Cliente, Pedido

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nome_vendedor', 'email', 'telefone')
    fields = ('nome_vendedor', 'email', 'telefone')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'telefone','endereco', 'email')
    fields = ('nome_cliente', 'telefone','endereco', 'email')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('nome_pedido', 'cliente', 'data_entrega', 'status', 'valor', 'imagem_thumbnail')
    fields = ('nome_pedido', 'cliente', 'tipo_massa', 'recheio', 'formato', 'tamanho', 'andares', 'imagem', 'observacoes', 'data_entrega', 'endereco_pedido', 'tipo_pagamento', 'status', 'valor')
    
    def imagem_thumbnail(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.imagem.url
            )
        return "Sem imagem"
    imagem_thumbnail.short_description = 'Imagem'

