from django.db import models
from django.contrib.auth.models import AbstractUser


class UsuarioAdaptado(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    nome_cidade = models.CharField(max_length=100, blank=True, null=True)
    nome_mae = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=150, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    nome_bairro = models.CharField(max_length=100, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to="perfil/", null=True, blank=True, verbose_name="Foto de Perfil")

    def __str__(self):
        return f"{self.username}"

    def is_administrador(self):
        return self.groups.filter(name="ADMINISTRADOR").exists()

    def is_user_simples(self):
        return self.groups.filter(name="USUARIO_SIMPLES").exists()
