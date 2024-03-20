from django.shortcuts import render, redirect
from core.models import Evento, Ticket
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from .form import CreateTicketForm, EditarTicketForm, FecharTicketForm

# Create your views here.

#def index(request):
#    return redirect('/agenda/')


def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou Senha inválido.")
    return redirect('/')


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos':evento}
    return render(request, 'agenda/agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'agenda/evento.html', dados)


''' São duas formas de realizar esta operação de edição de Evento abaixo, porém a forma que NÃO está 'comentada', 
tem uma validação, se o usuario que está fazendo a alteração no evento, é realmente o usuario logado.'''

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
        #if id_evento:
            #Evento.objects.filter(id=id_evento).update(titulo=titulo,
                                                       #data_evento=data_evento,
                                                       #descricao=descricao,
                                                       #usuario=usuario)
        else:
            Evento.objects.create(titulo=titulo,
                              data_evento=data_evento,
                              descricao=descricao,
                              usuario=usuario)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login/')
def json_lista_evento(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False)


"""/////////////////////////////////////////////////////////////////////////////////////////////"""

# ver detalhes do ticket
@login_required(login_url='/login/')
def detalhes_do_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    t = User.objects.get(username=ticket.criado_por)
    tickets_por_usuer = t.criado_por.all()

    if not (request.user.groups.filter(name=ticket.criado_por_grupo).exists() or
            request.user.groups.filter(name=ticket.atribuido_para_grupo).exists() or
            request.user.is_superuser):
        messages.error(request, 'Você não tem permissão para ver os detalhes deste ticket.')
        return redirect('nome_da_sua_view_de_redirecionamento')

    contexto = {'ticket': ticket, 'tickets_por_usuer':tickets_por_usuer}
    return render(request, 'ticket/detalhes_do_ticket.html', contexto)

"""/////////////////////////////////////////////////////////////////////////////////////////////"""

# criar o ticket
@login_required(login_url='/login/')
def criar_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.criado_por = request.user
            var.ticket_status = 'Pendente'
            var.atribuido_para_grupo = form.cleaned_data['atribuido_para_grupo']
            var.save()
            messages.info(request, 'Sua solicitação foi enviada com sucesso.')
            return redirect('criar_ticket')
        else:
            messages.error(request, 'Algo deu errado. Por favor, verifique as informações do formulário.')
            return redirect('criar_ticket')
    else:
        form = CreateTicketForm()
        contexto = {'form': form}
        return render(request, 'ticket/criar_ticket.html', contexto)



# editar um ticket
@login_required(login_url='/login/')
def editar_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if not ticket.foi_resolvido:
        if request.method == 'POST':
            form = EditarTicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.info(request, 'As informações do seu ticket foram atualizadas e todas as alterações foram salvas.')
                return redirect('editar_ticket')
            else:
                messages.warning(request, 'algo deu errado. Por favor, verifique as informações do formulário.')
        else:
            form = EditarTicketForm(instance=ticket)
            contexto = {'form': form}
            return render(request, 'ticket/editar_ticket.html', contexto)
    else:
        messages.warning(request, 'Você não pode mais fazer alterações!')
        return redirect('area_de_trabalho')

"""/////////////////////////////////////////////////////////////////////////////////////////////"""
# lista de tickets

# viazualizar todos os tickets criados
@login_required(login_url='/login/')
def todos_os_tickets(request):
    tickets = Ticket.objects.filter(criado_por=request.user).order_by('-data_criada')
    contexto = {'tickets': tickets}
    return render(request, 'ticket/todos_os_tickets.html', contexto)

@login_required(login_url='/login/')
def lista_de_tickets(request):
    tickets = Ticket.objects.filter(ticket_status='Pendente')
    contexto = {'tickets': tickets}
    return render(request, 'ticket/lista_de_tickets.html', contexto)

# aceitar um ticket da fila
@login_required(login_url='/login/')
def aceitar_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if request.user.groups.filter(name=ticket.atribuido_para_grupo.name).exists():
        ticket.atribuido_para = request.user
        ticket.ticket_status = 'Ativo'
        ticket.data_aceita = datetime.now()
        ticket.save()
        messages.info(request, 'O ticket foi aceito. Por favor, resolva o mais rápido possível!')
    else:
        messages.warning(request, 'Você não tem permissão para aceitar este ticket.')
    return redirect('area_de_trabalho')



# fechar ticket
#@login_required(login_url='/login/')
#def fechar_ticket(request, pk):
#    ticket = Ticket.objects.get(pk=pk)
#    ticket.ticket_status = 'Completo'
#    ticket.foi_resolvido = True
#    ticket.data_fechada = datetime.now()
#    ticket.save()
#    messages.info(request, 'O ticket foi resolvido. Obrigado, brilhante suporte!')
#    return redirect('todos_os_tickets')

@login_required(login_url='/login/')
def fechar_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if request.method == 'POST':
        form = FecharTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.ticket_status = 'Completo'
            ticket.foi_resolvido = True
            ticket.data_fechada = datetime.now()
            ticket.tempo_resposta_fechamento = datetime.now()
            ticket.save()
            messages.info(request, 'O ticket foi resolvido. Obrigado, brilhante suporte!')
        else:
            messages.error(request, 'Algo deu errado. Por favor, verifique as informações do formulário.')
    else:
        form = FecharTicketForm(instance=ticket)
    contexto = {'form': form}
    return redirect('todos_os_tickets')

# ticket no qual está trabalhando
@login_required(login_url='/login/')
def area_de_trabalho(request):
    grupo_do_usuario = request.user.groups.first()  # Obter o primeiro grupo do usuário
    tickets = Ticket.objects.filter(atribuido_para_grupo=grupo_do_usuario, foi_resolvido=False)
    contexto = {'tickets': tickets}
    return render(request, 'ticket/area_de_trabalho.html', contexto)


# todos os tickets resolvidos
@login_required(login_url='/login/')
def todos_os_tickets_fechados(request):
    tickets = Ticket.objects.filter(atribuido_para_id=request.user, foi_resolvido=True)
    contexto = {'tickets': tickets}
    return render(request, 'ticket/todos_os_tickets_fechados.html', contexto)

def obter_grupos(request):
    grupos = Group.objects.all()
    return render(request, 'ticket/criar_ticket.html', {'grupos': grupos})
