from django.contrib import admin
from core.models import Evento, Ticket

# Register your models here.

class EventoAdmin(admin.ModelAdmin):
    list_display = ('id','titulo', 'data_evento', 'data_criacao')
    list_filter = ('titulo','usuario','data_evento',)

admin.site.register(Evento, EventoAdmin)

#class TicketAdmin(admin.ModelAdmin):
#    list_display = ('numero_do_ticket','titulo_ticket', 'criado_por_id', 'prazo', 'data_criada', 'ticket_status', 'foi_resolvido', 'atribuido_para_id')
#    list_filter = ('numero_do_ticket','titulo', 'data_criada', 'ticket_status', 'foi_resolvido', 'atribuido_para_id')

#admin.site.register(Ticket, TicketAdmin)