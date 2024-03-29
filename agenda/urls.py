"""
URL configuration for agenda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('agenda/', views.lista_eventos),
    path('agenda/lista/', views.json_lista_evento),
    path('agenda/evento/', views.evento),
    path('agenda/evento/submit', views.submit_evento),
    path('agenda/evento/delete/<int:id_evento>/', views.delete_evento),
    path('', RedirectView.as_view(url='/area_de_trabalho/')),
    path('login/', views.login_user),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user),
    path('detalhes_do_ticket/<int:pk>/', views.detalhes_do_ticket, name='detalhes_do_ticket'),
    path('criar_ticket/', views.criar_ticket, name='criar_ticket'),
    path('editar_ticket/<int:pk>/', views.editar_ticket, name='editar_ticket'),
    path('todos_os_tickets/', views.todos_os_tickets, name='todos_os_tickets'),
    path('lista_de_tickets/', views.lista_de_tickets, name='lista_de_tickets'),
    path('aceitar_ticket/<int:pk>/', views.aceitar_ticket, name='aceitar_ticket'),
    path('fechar_ticket/<int:pk>/', views.fechar_ticket, name='fechar_ticket'),
    path('area_de_trabalho/', views.area_de_trabalho, name='area_de_trabalho'),
    path('todos_os_tickets_fechados/', views.todos_os_tickets_fechados, name='todos_os_tickets_fechados'),
    path('meus_chamados/', views.meus_chamados, name='meus_chamados'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
