from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model

user = get_user_model()
from django.db.models import Count
from datetime import date
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Entregador, Pedido
from cliente.models import UsuarioAdaptado
from .forms import EntregadorForm, PedidoForm, PedidoFiltroForm, EntregadorFiltroForm


def index(request):
    total_usuarios = user.objects.count()
    total_entregadores = Entregador.objects.count()

    context = {
        "total_usuarios": total_usuarios,
        "total_entregadores": total_entregadores,
    }

    return render(request, "index.html", context)


@login_required
def pedido_list(request):
    total_pedidos = Pedido.objects.count()
    total_p_cancelados = Pedido.objects.filter(status="Cancelado").count()
    total_p_entregues = Pedido.objects.filter(status="Entregue").count()
    pedidos = Pedido.objects.all()

    # ========== ADICIONE ESTE BLOCO ==========
    # Criar instância do formulário
    filtro_form = PedidoFiltroForm(request.GET or None)

    # Aplicar filtros se válido
    if filtro_form.is_valid():
        # Filtro por descrição
        descricao = filtro_form.cleaned_data.get("descricao")
        if descricao:
            pedidos = pedidos.filter(nome_pedido__icontains=descricao)

        # Filtro por data início
        data_inicio = filtro_form.cleaned_data.get("data_inicio")
        if data_inicio:
            pedidos = pedidos.filter(data_entrega__date__gte=data_inicio)

        # Filtro por data fim
        data_fim = filtro_form.cleaned_data.get("data_fim")
        if data_fim:
            pedidos = pedidos.filter(data_entrega__date__lte=data_fim)

        # Filtro por cliente
        cliente = filtro_form.cleaned_data.get("cliente")
        if cliente:
            pedidos = pedidos.filter(cliente=cliente)

        # Filtro por entregador
        entregador = filtro_form.cleaned_data.get("entregador")
        if entregador:
            pedidos = pedidos.filter(entregador=entregador)

        # Filtro por status
        status = filtro_form.cleaned_data.get("status")
        if status:
            pedidos = pedidos.filter(status=status)
    # ========== FIM DO BLOCO ==========

    # 2. Criar o paginador (9 vagas por página)
    paginator = Paginator(pedidos, 9)

    # 3. Pegar o número da página da URL (?page=2)
    page_number = request.GET.get("page")

    # 4. Obter os dados daquela página específica
    page_obj = paginator.get_page(page_number)

    # 5. Enviar para o template
    return render(
        request,
        "pedido/listar_pedido.html",
        {
            "pedidos": page_obj,
            "page_obj": page_obj,
            "filtro_form": filtro_form,
            "total_pedidos": total_pedidos,
            "total_p_cancelados": total_p_cancelados,
            "total_p_entregues": total_p_entregues,
        },
    )


def atribuir_entregador_automatico():
    # Conta quantos pedidos cada entregador tem em andamento
    entregador = (
        Entregador.objects.filter(disponibilidade=True)
        .annotate(num_pedidos=Count("pedidos"))
        .order_by("num_pedidos")  # pega o que tem menos entregas
        .first()
    )
    if entregador:
        entregador.num_entregas += 1  # soma +1
        entregador.save()

    return entregador


@login_required
def pedido_create(request):
    if request.method == "POST":
        form = PedidoForm(request.POST, request.FILES)

        if not request.user.is_administrador() and not request.user.is_superuser:
            if "status" in form.fields:
                del form.fields["status"]

        if form.is_valid():
            pedido = form.save(commit=False)  # não salva ainda

            # atribui o usuário logado
            if request.user.is_authenticated:
                pedido.cliente = request.user
            else:
                messages.error(request, "É necessário estar logado para fazer um pedido.")
                return redirect("login")  # ou qualquer rota de login

            pedido.entregador = atribuir_entregador_automatico()  # atribui automaticamente
            if not pedido.entregador:
                messages.error(request, "Nenhum entregador disponível no momento.")
                return redirect("pedido_list")

            if pedido.tamanho == "Mini":
                pedido.valor = 50
            elif pedido.tamanho == "PP":
                pedido.valor = 80
            elif pedido.tamanho == "P":
                pedido.valor = 130
            elif pedido.tamanho == "M":
                pedido.valor = 170
            elif pedido.tamanho == "G":
                pedido.valor = 270

            pedido.save()
            messages.success(request, f'Pedido "{pedido.nome_pedido}" feito com sucesso!')
            if not request.user.is_administrador() and not request.user.is_superuser:
                return redirect("historico")
            else:
                return redirect("pedido_list")
    else:
        form = PedidoForm()

    return render(request, "pedido/form_pedido.html", {"form": form})


@login_required
def pedido_update(request, id):
    pedido = get_object_or_404(Pedido, id=id)

    if request.method == "POST":
        form = PedidoForm(request.POST, request.FILES, instance=pedido)

        if form.is_valid():
            if pedido.tamanho == "Mini":
                pedido.valor = 50
            elif pedido.tamanho == "PP":
                pedido.valor = 80
            elif pedido.tamanho == "P":
                pedido.valor = 130
            elif pedido.tamanho == "M":
                pedido.valor = 170
            elif pedido.tamanho == "G":
                pedido.valor = 270

            pedido = form.save()
            messages.success(request, f'Pedido "{pedido.nome_pedido}" atualizado com sucesso!')
            return redirect("pedido_detail", id=pedido.id)
    else:
        form = PedidoForm(instance=pedido)

    return render(request, "pedido/form_pedido.html", {"form": form})


def pedido_delete(request, id):
    pedido = get_object_or_404(Pedido, id=id)

    if request.method == "POST":
        nome = pedido.nome_pedido
        pedido.delete()
        messages.success(request, f'Pedido "{nome}" excluído com sucesso!')
        return redirect("pedido_list")

    return render(request, "pedido/delete_pedido.html", {"pedido": pedido})

def cancelar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)

    if request.method == "POST":
        pedido.status = "Cancelado"
        pedido.save()
        messages.success(request, "Pedido cancelado com sucesso!")
    if not request.user.is_administrador() and not request.user.is_superuser:
        return redirect('historico')
    else:
        return redirect('pedido_detail', id=id)
    


@login_required
def pedido_detail(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    cliente = get_object_or_404(UsuarioAdaptado, id=(pedido.cliente.id))
    context = {"pedido": pedido, "cliente": cliente}
    return render(request, "pedido/detail_pedido.html", context)


@login_required
def entregador_list(request):
    # Iniciar com todas as vagas
    entregadores = Entregador.objects.all()
    total_entregadores = Entregador.objects.count()
    total_disponiveis = Entregador.objects.filter(disponibilidade=True).count()

    # ========== ADICIONE ESTE BLOCO ==========
    # Criar instância do formulário
    filtro_form = EntregadorFiltroForm(request.GET or None)

    # Aplicar filtros se válido
    if filtro_form.is_valid():
        # Filtro por descrição
        descricao = filtro_form.cleaned_data.get("descricao")
        if descricao:
            entregadores = entregadores.filter(nome_entregador__icontains=descricao)

        # Filtro por data início
        data_inicio = filtro_form.cleaned_data.get("data_inicio")
        if data_inicio:
            entregadores = entregadores.filter(data_contratatacao__date__gte=data_inicio)

        # Filtro por data fim
        data_fim = filtro_form.cleaned_data.get("data_fim")
        if data_fim:
            entregadores = entregadores.filter(data_contratacao__date__lte=data_fim)

        # Filtro por status
        disponibilidade = filtro_form.cleaned_data.get("disponibilidade")
        if disponibilidade == "true":
            entregadores = entregadores.filter(disponibilidade=True)
        elif disponibilidade == "false":
            entregadores = entregadores.filter(disponibilidade=False)
    # ========== FIM DO BLOCO ==========

    paginator = Paginator(entregadores, 9)

    # 3. Pegar o número da página da URL (?page=2)
    page_number = request.GET.get("page")

    # 4. Obter os dados daquela página específica
    page_obj = paginator.get_page(page_number)

    # MODIFIQUE o return
    return render(
        request,
        "entregador/listar_entregador.html",
        {
            "entregadores": page_obj,
            "page_obj": page_obj,
            "filtro_form": filtro_form,
            "total_entregadores": total_entregadores,
            "total_disponiveis": total_disponiveis,
        },
    )


@login_required
def entregador_create(request):
    if request.method == "POST":
        form = EntregadorForm(request.POST)
        if form.is_valid():
            entregador = form.save()
            messages.success(request, f'Entregador "{entregador.nome_entregador}" criado com sucesso!')
            return redirect("entregador_list")
    else:
        form = EntregadorForm()

    return render(request, "entregador/form_entregador.html", {"form": form})


@login_required
def entregador_update(request, id):
    entregador = get_object_or_404(Entregador, id=id)

    if request.method == "POST":
        form = EntregadorForm(request.POST, instance=entregador)
        if form.is_valid():
            entregador = form.save()
            messages.success(request, f'Entregador "{entregador.nome_entregador}" atualizado com sucesso!')
            return redirect("entregador_detail", id=entregador.id)
    else:
        form = EntregadorForm(instance=entregador)

    return render(request, "entregador/form_entregador.html", {"form": form})


def entregador_delete(request, id):
    entregador = get_object_or_404(Entregador, id=id)

    if request.method == "POST":
        nome = entregador.nome_entregador
        entregador.delete()
        messages.success(request, f'Entregador "{nome}" excluído com sucesso!')
        return redirect("entregador_list")

    return render(request, "entregador/delete_entregador.html", {"entregador": entregador})


@login_required
def entregador_detail(request, id):
    entregador = get_object_or_404(Entregador, id=id)
    context = {"entregador": entregador}
    return render(request, "entregador/detail_entregador.html", context)
