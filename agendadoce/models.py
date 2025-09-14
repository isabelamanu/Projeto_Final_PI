from django.db import models

class Vendedor(models.Model):
    nome_vendedor = models.CharField(max_length=150)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_vendedor + " - " + self.telefone 

class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=150)
    telefone = models.CharField(max_length=150)
    endereco = models.CharField(max_length=250)
    email = models.EmailField()

    def __str__(self):
        return self.nome_cliente + " - " + self.telefone

class Pedido(models.Model):
    nome_pedido = models.CharField()
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    tipo_massa = models.CharField()
    recheio = models.CharField()
    formato = models.CharField()
    tamanho = models.CharField()
    andares = models.IntegerField()
    imagem = models.ImageField(upload_to='imagens_pedidos/', blank=True, null=True)
    observacoes = models.TextField(max_length=250)
    data_entrega = models.DateTimeField()
    endereco_pedido = models.TextField(max_length=100)
    tipo_pagamento = models.CharField()
    status = models.CharField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome_pedido