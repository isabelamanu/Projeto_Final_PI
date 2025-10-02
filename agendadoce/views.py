from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Count
from datetime import date
from django.contrib import messages
from .models import Entregador, Pedido
from .forms import EntregadorForm, PedidoForm

def index(request):
    total_pedidos = Pedido.objects.count()
    total_usuarios = User.objects.count()
    total_entregadores = Entregador.objects.count()
    
    context = {
        'hoje': date.today(),
        'total_pedidos': total_pedidos,
        'total_usuarios': total_usuarios,
        'total_entregadores': total_entregadores,
    }
    
    return render(request, 'index.html', context)

def pedido_list(request):
    pedidos = Pedido.objects.all()
    context ={
        'pedidos': pedidos
    }
    return render(request, 'pedido/listar_pedido.html',context)

def atribuir_entregador_automatico():
    # Conta quantos pedidos cada entregador tem em andamento
    entregador = (
        Entregador.objects.filter(disponibilidade=True)
        .annotate(num_pedidos=Count("pedidos"))
        .order_by("num_pedidos")  # pega o que tem menos entregas
        .first()
    )
    if entregador:
        entregador.num_entregas += 1   # soma +1
        entregador.save()

    return entregador

def pedido_create(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)  # não salva ainda

            # atribui o usuário logado
            if request.user.is_authenticated:
                pedido.cliente = request.user
            else:
                messages.error(request, 'É necessário estar logado para fazer um pedido.')
                return redirect('login')  # ou qualquer rota de login
            
            pedido.entregador = atribuir_entregador_automatico()  # atribui automaticamente
            if not pedido.entregador:
                messages.error(request, 'Nenhum entregador disponível no momento.')
                return redirect('pedido_list')

            pedido.save()
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
    return render(request, 'pedido/detail_pedido.html', context)
    

def entregador_list(request):
    entregadores = Entregador.objects.all()
    context = {
        'entregadores': entregadores,
    }
    return render(request, 'entregador/listar_entregador.html', context)

def entregador_create(request):
    if request.method == 'POST':
        form = EntregadorForm(request.POST)
        if form.is_valid():
            entregador = form.save()
            messages.success(request, f'Entregador "{entregador.nome_vendedor}" criado com sucesso!')
            return redirect('entregador_list')
    else:
        form = EntregadorForm()
    
    return render(request, 'entregador/form_entregador.html', {'form': form})

def entregador_update(request, id):
    entregador = get_object_or_404(Entregador, id=id)
    
    if request.method == 'POST':
        form = EntregadorForm(request.POST, instance=entregador)
        if form.is_valid():
            entregador = form.save()
            messages.success(request, f'Entregador "{entregador.nome_vendedor}" atualizado com sucesso!')
            return redirect('entregador_detail', id=entregador.id)
    else:
        form = EntregadorForm(instance=entregador)
    
    return render(request, 'entregador/form_entregador.html', {'form':form})

def entregador_delete(request, id):
    entregador = get_object_or_404(Entregador, id=id)
    nome = entregador.nome_entregador
    entregador.delete()
    messages.success(request, f'Entregador "{nome}" excluído com sucesso!')
    return redirect('entregador_list')

def entregador_detail(request, id):
    entregador = get_object_or_404(Entregador, id=id)
    context= {
        'entregador': entregador
    }
    return render(request, 'entregador/detail_entregador.html', context)

