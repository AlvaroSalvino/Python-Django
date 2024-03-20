from django.contrib import admin
from core.models import Evento, Ticket

# Register your models here.

class EventoAdmin(admin.ModelAdmin):
    list_display = ('id','titulo', 'data_evento', 'data_criacao')
    list_filter = ('titulo','usuario','data_evento',)

admin.site.register(Evento, EventoAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id','titulo_ticket', 'criado_por', 'atribuido_para', 'atribuido_para_grupo')
    list_filter = ('titulo_ticket', 'criado_por', 'atribuido_para', 'atribuido_para_grupo')

admin.site.register(Ticket, TicketAdmin)