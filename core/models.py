import uuid
from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime


class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'evento'
    def __str__(self):
        return self.titulo

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y %H:%M Hrs')

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')

    def get_evento_atrasado(self):
        if self.data_evento < datetime.now():
            return True
        else:
            return False

class Ticket(models.Model):
    status_choices = (
        ('Ativo', 'Ativo'),
        ('Completo', 'Completo'),
        ('Pendente', 'Pendente')
    )
    numero_do_ticket = models.UUIDField(default=uuid.uuid4)
    atribuido_para_grupo = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, blank=True)
    titulo_ticket = models.CharField(max_length=150)
    descricao_ticket = models.TextField()
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='criado_por')
    data_criada = models.DateTimeField(auto_now_add=True)
    atribuido_para = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    foi_resolvido = models.BooleanField(default=False)
    prazo = models.DateField(null=True, blank=True, verbose_name='Prazo')
    data_aceita = models.DateTimeField(null=True, blank=True)
    data_fechada = models.DateTimeField(null=True, blank=True)
    ticket_status = models.CharField(max_length=15, choices=status_choices)
    resposta_fechamento = models.TextField()
    tempo_resposta_fechamento = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'ticket'

    def __str__(self):
        return self.titulo_ticket

    def get_prazo(self):
        return self.prazo.strftime('%d/%m/%Y')

    def get_data_criada(self):
        return self.data_criada.strftime('%d/%m/%Y %H Hrs')

    def get_data_aceita(self):
        return self.data_aceita.strftime('%d/%m/%Y %H Hrs')

    def get_data_fechada(self):
        return self.data_fechada.strftime('%d/%m/%Y %H Hrs')

    def get_data_input_prazo(self):
        return self.prazo.strftime('%Y-%m-%dT%H')
    def get_tempo_resposta_fechamento(self):
        return self.tempo_resposta_fechamento.strftime('%d/%m/%Y %H Hrs')
