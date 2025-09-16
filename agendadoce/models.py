from django.db import models

class Entregador(models.Model):
    nome_entregador = models.CharField(max_length=150)
    cpf = models.CharField()
    telefone = models.CharField(max_length=20)
    data_contratacao = models.DateField()
    num_entregas = models.PositiveIntegerField(default=0)
    veiculo = models.CharField(max_length=50, blank=True, null=True)
    disponibilidade = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_entregador + " - " + self.disponibilidade

class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=150)
    cpf = models.CharField()
    email = models.EmailField()
    telefone = models.CharField(max_length=150)
    endereco = models.CharField(max_length=250)

    def __str__(self):
        return self.nome_cliente + " - " + self.telefone

class Pedido(models.Model):
    TIPO_MASSA_CHOICES = [
        ("chocolate", "Chocolate"),
        ("amantegada", "Amanteigada"),
        ("formigueiro", "Formigueiro"),
    ]

    RECHEIO_CHOICES = [
        ("brigadeiro", "Brigadeiro"),
        ("ninho", "Ninho"),
        ("prestígio", "Prestígio"),
        ("paçoca", "Paçoca"),
        ("frutas vermelhas", "Frutas Vermelhas"),
    ]

    TAMANHO_CHOICES = [
        ("mini", "Mini (8 pessoas)"),
        ("pp", "PP (15 pessoas)"),
        ("p", "P (25 pessoas)"),
        ("m", "M (45 pessoas)"),
        ("g", "G (85 pessoas)"),
    ]

    STATUS_CHOICES = [
        ("aguardando", "Aguardando Confirmação"),
        ("producao", "Em Produção"),
        ("entrega", "Saiu para Entrega"),
        ("entregue", "Entregue"),
        ("cancelado", "Cancelado"),
    ]

    PAGAMENTO_CHOICES = [
        ("dinheiro", "Dinheiro"),
        ("pix", "Pix"),
        ("cartao", "Cartão"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pedidos")
    entregador = models.ForeignKey(Entregador, on_delete=models.CASCADE, related_name="pedidos")
    nome_pedido = models.CharField(max_length=100)
    tipo_massa = models.CharField(max_length=20, choices=TIPO_MASSA_CHOICES)
    recheio = models.CharField(max_length=20, choices=RECHEIO_CHOICES)
    formato = models.CharField(max_length=50)
    tamanho = models.CharField(max_length=20, choices=RECHEIO_CHOICES)
    foto = models.ImageField(upload_to='fotos_pedidos/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    data_entrega = models.DateTimeField()
    endereco_pedido = models.TextField(blank=True, null=True)
    tipo_pagamento = models.CharField(max_length=20, choices=PAGAMENTO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="aguardando")
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} - {self.nome_pedido} ({self.cliente})"
