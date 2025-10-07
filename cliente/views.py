from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioAdaptadoCreationForm, LoginForm,PerfilForm
from .models import UsuarioAdaptado
from django.contrib.auth.models import Group



def cliente_create(request):
    if request.method == 'POST':
        form = UsuarioAdaptadoCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Adicionar usuário ao grupo USUARIO_SIMPLES por padrão
            grupo_simples, created = Group.objects.get_or_create(name='USUARIO_SIMPLES')
            user.groups.add(grupo_simples)
            
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = UsuarioAdaptadoCreationForm()
    
    return render(request, 'clientes/create_cliente.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
       return redirect('pedido_list')
   
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')
                
                # Redireciona para a página solicitada
                next_page = request.GET.get('next', 'historico')
                return redirect(next_page)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'clientes/login.html', {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')

@login_required
def perfil_view(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)
    
    return render(request, 'clientes/detail_cliente.html', {'form': form})

def cliente_detail(request, id):
    cliente = get_object_or_404(UsuarioAdaptado, id=id)
    context= {
        'cliente': cliente
    }
    return render(request, 'clientes/detail_cliente.html', context)

@login_required
def cliente_list(request):
    clientes = UsuarioAdaptado.objects.all()
    context = {
        'clientes': clientes,
    }
    return render(request, 'clientes/listar_cliente.html', context)

@login_required
def cliente_update(request, id):
    cliente = get_object_or_404(UsuarioAdaptado, id=id)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.username}" atualizado com sucesso!')
            return redirect('cliente_detail', id=cliente.id)
    else:
        form = PerfilForm(instance=cliente)
    
    return render(request, 'clientes/update_cliente.html', {'form':form})

def cliente_delete(request, id):
    cliente = get_object_or_404(UsuarioAdaptado, id=id)
    nome = UsuarioAdaptado.username
    cliente.delete()
    messages.success(request, f'Cliente "{nome}" excluído com sucesso!')
    return redirect('cliente_list')

def historico_cliente(request):
    return render(request, 'clientes/historico_cliente.html')