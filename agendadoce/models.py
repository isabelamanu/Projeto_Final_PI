from django.db import models
from django.conf import settings

class Entregador(models.Model):
    nome_entregador = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    telefone = models.CharField(max_length=20)
    data_contratacao = models.DateField()
    num_entregas = models.PositiveIntegerField(default=0)
    veiculo = models.CharField(max_length=50, blank=True, null=True)
    disponibilidade = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_entregador + " - " + str(self.disponibilidade)

class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    email = models.EmailField()
    telefone = models.CharField(max_length=150)
    endereco = models.CharField(max_length=250)

    def __str__(self):
        return self.nome_cliente

class Pedido(models.Model):
    TIPO_MASSA_CHOICES = [
        ("Chocolate", "Chocolate"),
        ("Amanteigada", "Amanteigada"),
        ("Formigueiro", "Formigueiro"),
    ]

    RECHEIO_CHOICES = [
        ("Brigadeiro", "Brigadeiro"),
        ("Ninho", "Ninho"),
        ("Prestígio", "Prestígio"),
        ("Paçoca", "Paçoca"),
        ("Frutas Vermelhas", "Frutas Vermelhas"),
    ]

    TAMANHO_CHOICES = [
        ("Mini", "Mini (8 pessoas)"),
        ("PP", "PP (15 pessoas)"),
        ("P", "P (25 pessoas)"),
        ("M", "M (45 pessoas)"),
        ("G", "G (85 pessoas)"),
    ]

    STATUS_CHOICES = [
        ("Aguardando Confirmação", "Aguardando Confirmação"),
        ("Em producao", "Em Produção"),
        ("Entregue", "Entregue"),
        ("Cancelado", "Cancelado"),
    ]

    PAGAMENTO_CHOICES = [
        ("Dinheiro", "Dinheiro"),
        ("Pix", "Pix"),
        ("Cartao", "Cartão"),
    ]

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pedidos")
    entregador = models.ForeignKey(Entregador, on_delete=models.CASCADE, related_name="pedidos", null=True, blank=True)
    nome_pedido = models.CharField(max_length=100)
    tipo_massa = models.CharField(max_length=20, choices=TIPO_MASSA_CHOICES)
    recheio = models.CharField(max_length=20, choices=RECHEIO_CHOICES)
    formato = models.CharField(max_length=50)
    tamanho = models.CharField(max_length=20, choices=TAMANHO_CHOICES)
    foto = models.ImageField(upload_to='fotos_pedidos/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    data_entrega = models.DateTimeField()
    endereco_pedido = models.TextField(blank=True, null=True)
    tipo_pagamento = models.CharField(max_length=20, choices=PAGAMENTO_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Aguardando Confirmação")
    valor = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.nome_pedido} ({self.cliente})"
