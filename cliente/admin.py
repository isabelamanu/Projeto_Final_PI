from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioAdaptado


@admin.register(UsuarioAdaptado)
class UsuarioAdaptadoAdmin(UserAdmin):
    model = UsuarioAdaptado
    list_display = ["username", "email", "cpf", "nome_cidade", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "groups"]
    search_fields = ["username", "email", "cpf", "nome_mae", "telefone"]

    fieldsets = UserAdmin.fieldsets + (
        ("Informações Adicionais", {"fields": ("cpf", "nome_cidade", "nome_mae", "endereco", "nome_bairro")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informações Adicionais", {"fields": ("cpf", "nome_cidade", "nome_mae", "endereco", "nome_bairro")}),
    )
