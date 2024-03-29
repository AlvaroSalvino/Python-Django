# Generated by Django 5.0.1 on 2024-03-19 22:24

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0002_evento_usuario_alter_evento_data_evento'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_do_ticket', models.UUIDField(default=uuid.uuid4)),
                ('titulo_ticket', models.CharField(max_length=150)),
                ('descricao_ticket', models.TextField()),
                ('data_criada', models.DateTimeField(auto_now_add=True)),
                ('foi_resolvido', models.BooleanField(default=False)),
                ('prazo', models.DateTimeField(blank=True, null=True)),
                ('data_aceita', models.DateTimeField(blank=True, null=True)),
                ('data_fechada', models.DateTimeField(blank=True, null=True)),
                ('ticket_status', models.CharField(choices=[('Ativo', 'Ativo'), ('Completo', 'Completo'), ('Pendente', 'Pendente')], max_length=15)),
                ('resposta_fechamento', models.TextField(blank=True, null=True)),
                ('tempo_resposta_fechamento', models.DateTimeField(blank=True, null=True)),
                ('atribuido_para', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('atribuido_para_grupo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='auth.group')),
                ('criado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ticket',
            },
        ),
    ]
