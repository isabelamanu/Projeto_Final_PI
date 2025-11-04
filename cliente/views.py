from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioAdaptadoCreationForm, LoginForm, PerfilForm, UsuarioFiltroForm, UsuarioEditForm
from .models import UsuarioAdaptado
from agendadoce.models import Pedido
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


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
        if not request.user.is_administrador() and not request.user.is_superuser:
            return redirect('historico')
        else:
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
    return redirect('index')

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
    """View para listar usuários com filtros e paginação"""
    
    # Buscar todos os usuários
    usuarios = UsuarioAdaptado.objects.all()
    total_usuarios = UsuarioAdaptado.objects.count()
    total_pedidos = Pedido.objects.count()
    pedido_por_cliente = str(int(total_pedidos)/int(total_usuarios))
    
    # ========== FILTROS ==========
    filtro_form = UsuarioFiltroForm(request.GET or None)
    
    if filtro_form.is_valid():
        # Filtro por username
        username = filtro_form.cleaned_data.get('username')
        if username:
            usuarios = usuarios.filter(username__icontains=username)
        
        # Filtro por email
        email = filtro_form.cleaned_data.get('email')
        if email:
            usuarios = usuarios.filter(email__icontains=email)
        
        # Filtro por cidade
        cidade = filtro_form.cleaned_data.get('cidade')
        if cidade:
            usuarios = usuarios.filter(nome_cidade__icontains=cidade)
        
        # Filtro por grupo
        grupo = filtro_form.cleaned_data.get('grupo')
        if grupo:
            usuarios = usuarios.filter(groups=grupo)
    
    # ========== PAGINAÇÃO ==========

    paginator = Paginator(usuarios, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'clientes/listar_cliente.html', {
        'usuarios': page_obj,
        'page_obj': page_obj,
        'filtro_form': filtro_form,
        'total_usuarios': total_usuarios,
        'pedido_por_cliente': pedido_por_cliente,
       })

@login_required
def create_usuario_admin(request):
    """View para criar usuário (apenas para gerentes)"""
    
    if not request.user.is_administrador() and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('historico')
    
    if request.method == 'POST':
        form = UsuarioAdaptadoCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Adicionar ao grupo USUARIO_SIMPLES por padrão
            grupo_simples, created = Group.objects.get_or_create(name='USUARIO_SIMPLES')
            user.groups.add(grupo_simples)
            
            messages.success(request, f'Usuário {user.username} criado com sucesso!')
            return redirect('cliente_list')
    else:
        form = UsuarioAdaptadoCreationForm()
    
    return render(request, 'clientes/update_cliente.html', {
        'form': form, 
        'titulo': 'Criar Novo Usuário'
    })


@login_required
def update_usuario_admin(request, id):
    """View para editar usuário (apenas para gerentes)"""
    
    if not request.user.is_administrador() and not request.user.is_superuser:
        return redirect('historico')
    
    usuario = get_object_or_404(UsuarioAdaptado, id=id)
    
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {usuario.username} atualizado com sucesso!')
            return redirect('cliente_list')
    else:
        form = UsuarioEditForm(instance=usuario)
    
    return render(request, 'clientes/update_cliente.html', {
        'form': form, 
        'titulo': f'Editar Usuário: {usuario.username}',
        'usuario': usuario
    })

@login_required
def cliente_update(request, id):
    cliente = get_object_or_404(UsuarioAdaptado, id=id)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.username}" atualizado com sucesso!')
            return redirect('cliente_detail', id=cliente.id)
    else:
        form = UsuarioEditForm(instance=cliente)
    
    return render(request, 'clientes/update_cliente.html', {'form':form})

def cliente_delete(request, id):
    """View para deletar usuário (apenas para gerentes)"""
    
    usuario = get_object_or_404(UsuarioAdaptado, id=id)
    
    # Impedir que o usuário delete a si mesmo
    if usuario == request.user:
        messages.error(request, 'Você não pode deletar seu próprio usuário!')
        return redirect('cliente_list')
    
    # Impedir que delete superusuários
    if usuario.is_superuser:
        messages.error(request, 'Não é possível deletar um superusuário!')
        return redirect('cliente_list')
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuário {username} deletado com sucesso!')
        return redirect('cliente_list')
    
    return render(request, 'clientes/delete_usuario.html', {
        'usuario': usuario
    })

def historico_cliente(request):
    return render(request, 'clientes/historico_cliente.html')