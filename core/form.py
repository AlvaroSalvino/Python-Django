from django import forms
from django.contrib.auth.models import Group
from .models import Ticket

class CreateTicketForm(forms.ModelForm):
    class Meta:
        db_table = 'ticket'
        atribuido_para_grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
        model = Ticket
        fields = ['titulo_ticket', 'descricao_ticket', 'prazo', 'atribuido_para_grupo']

class EditarTicketForm(forms.ModelForm):
    class Meta:
        db_table = 'ticket'
        atribuido_para_grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
        model = Ticket
        fields = ['titulo_ticket', 'descricao_ticket', 'prazo', 'atribuido_para_grupo']

