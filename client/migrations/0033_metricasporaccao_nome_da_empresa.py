# Generated by Django 4.1.4 on 2022-12-23 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0032_alter_cotacoesdasacoes_preco_da_acao'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricasporaccao',
            name='nome_da_empresa',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
