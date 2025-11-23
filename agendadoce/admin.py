from django.contrib import admin
from django.utils.html import format_html
from .models import Entregador, Pedido


@admin.register(Entregador)
class EntregadorAdmin(admin.ModelAdmin):
    list_display = ("nome_entregador", "cpf", "telefone", "num_entregas", "data_contratacao", "disponibilidade", "foto_entregador")
    fields = ("nome_entregador", "cpf", "telefone", "num_entregas", "data_contratacao", "disponibilidade", "foto_entregador")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("nome_pedido", "cliente", "entregador", "foto_thumbnail", "data_entrega", "status", "valor")
    fields = (
        "nome_pedido",
        "cliente",
        "entregador",
        "foto",
        "tipo_massa",
        "recheio",
        "formato",
        "tamanho",
        "observacoes",
        "data_entrega",
        "endereco_pedido",
        "tipo_pagamento",
        "status",
        "valor",
    )

    def foto_thumbnail(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.foto.url
            )
        return "Sem foto"

    foto_thumbnail.short_description = "Foto"
