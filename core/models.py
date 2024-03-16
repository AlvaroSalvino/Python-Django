import uuid

from django.db import models
from django.contrib.auth.models import User
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
    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='criado_por')
    data_criada = models.DateTimeField(auto_now_add=True)
    atribuido_para = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    foi_resolvido = models.BooleanField(default=False)
    data_aceita = models.DateTimeField(null=True, blank=True)
    data_fechada = models.DateTimeField(null=True, blank=True)
    ticket_status = models.CharField(max_length=15, choices=status_choices)

    def __str__(self):
        return self.titulo

