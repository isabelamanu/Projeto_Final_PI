from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import date
from django.contrib import messages
from .models import Vendedor, Cliente, Pedido
from .forms import VendedorForm, ClienteForm, PedidoForm

def index(request):
    total_pedidos = Pedido.objects.count()
    total_usuarios = User.objects.count()
    total_clientes = Cliente.objects.count()
    total_vendedores = Vendedor.objects.count()
    
    context = {
        'hoje': date.today(),
        'total_pedidos': total_pedidos,
        'total_usuarios': total_usuarios,
        'total_clientes': total_clientes,
        'total_vendedores': total_vendedores,
    }
    
    return render(request, 'index.html', context)

def pedido_list(request):
    pedidos = Pedido.objects.all()
    context ={
        'pedidos': pedidos
    }
    return render(request, 'pedido/listar_pedido.html',context)

def pedido_creat(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            form = PedidoForm()
            pedido = form.save()
            messages.success(request, f'Pedido "{pedido.nome_pedido}" feito com sucesso!')
            return redirect('pedido_list')
    else:
        form = PedidoForm()

    return render(request, 'pedido/form_pedido.html', {'form': form})

def pedido_update(request,id):
    pedido = get_object_or_404(Pedido,id=id)
   
    if request.method == 'POST':
        form = PedidoForm(request.POST,request.FILES,instance=pedido)

        if form.is_valid():
            pedido = form.save()
            messages.success(request, f'Pedido "{pedido.nome_pedido}" atualizado com sucesso!')
            return redirect('pedido_detail', id=pedido.id)
    else:
        form = PedidoForm(instance=pedido)

    return render(request,'pedido/form_pedido.html',{'form':form})

def pedido_delete(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    nome = pedido.nome_pedido
    pedido.delete()
    messages.success(request, f'Pedido "{nome}" excluído com sucesso!')
    return redirect('pedido_list')

def pedido_detail(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    context= {
        'pedido': pedido
    }
    return render(request, 'pedido/pedido_detail.html', context)
    

def vendedor_list(request):
    vendedores = Vendedor.objects.all()
    context = {
        'vendedores': vendedores,
    }
    return render(request, 'vendedor/listar_vendedor.html', context)

def vendedor_create(request):
    if request.method == 'POST':
        form = VendedorForm(request.POST)
        if form.is_valid():
            vendedor = form.save()
            messages.success(request, f'Vendedor "{vendedor.nome_vendedor}" criado com sucesso!')
            return redirect('vendedor_list')
    else:
        form = VendedorForm()
    
    return render(request, 'vendedor/form_vendedor.html', {'form': form})

def vendedor_update(request, id):
    vendedor = get_object_or_404(Vendedor, id=id)
    
    if request.method == 'POST':
        form = VendedorForm(request.POST, instance=vendedor)
        if form.is_valid():
            vendedor = form.save()
            messages.success(request, f'Vendedor "{vendedor.nome_vendedor}" atualizado com sucesso!')
            return redirect('vendedor_detail', id=vendedor.id)
    else:
        form = VendedorForm(instance=vendedor)
    
    return render(request, 'vendedor/form_vendedor.html', {'form':form})

def vendedor_delete(request, id):
    vendedor = get_object_or_404(Vendedor, id=id)
    nome = vendedor.nome_vendedor
    vendedor.delete()
    messages.success(request, f'Vendedor "{nome}" excluído com sucesso!')
    return redirect('vendedor_list')

def vendedor_detail(request, id):
    vendedor = get_object_or_404(Vendedor, id=id)
    context= {
        'vendedor': vendedor
    }
    return render(request, 'vendedor/detail_vendedor.html', context)


def cliente_list(request):
    clientes = Cliente.objects.all()
    context = {
        'clientes': clientes,
    }
    return render(request, 'cliente/listar_cliente.html', context)

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nome_cliente}" criado com sucesso!')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    
    return render(request, 'cliente/form_cliente.html', {'form': form})

def cliente_update(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nome_cliente}" atualizado com sucesso!')
            return redirect('cliente_detail', id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'vendedor/form_vendedor.html', {'form':form})

def cliente_delete(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    nome = cliente.nome_cliente
    cliente.delete()
    messages.success(request, f'Cliente "{nome}" excluído com sucesso!')
    return redirect('cliente_list')

def cliente_detail(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    context= {
        'cliente': cliente
    }
    return render(request, 'cliente/detail_cliente.html', context)