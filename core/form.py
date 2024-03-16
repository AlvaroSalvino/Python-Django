from django import forms
from .models import Ticket

class CreateTicketForm(forms.ModelForm):
    class Meta:
        db_table = 'ticket'
        model = Ticket
        fields = ['titulo_ticket', 'descricao_ticket', 'prazo']

class UpdateTicketForm(forms.ModelForm):
    class Meta:
        db_table = 'ticket'
        model = Ticket
        fields = ['titulo_ticket', 'descricao_ticket', 'prazo']

