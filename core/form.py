from django import forms
from django.contrib.auth.models import Group
from .models import Ticket

class CreateTicketForm(forms.ModelForm):
    class Meta:
        db_table = 'ticket'
        atribuido_para_grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
        model = Ticket
        fields = ['titulo_ticket', 'descricao_ticket', 'prazo', 'atribuido_para_grupo']
        widgets = {
            'prazo': forms.DateInput(format='%Y-%m-%d'),
        }


class EditarTicketForm(forms.ModelForm):
    class Meta:
        db_table = 'ticket'
        atribuido_para_grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
        model = Ticket
        fields = ['titulo_ticket', 'descricao_ticket', 'prazo', 'atribuido_para_grupo']
        widgets = {
            'prazo': forms.DateInput(format='%Y-%m-%d'),
        }

class FecharTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['resposta_fechamento']

