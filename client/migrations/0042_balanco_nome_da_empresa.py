# Generated by Django 4.1.4 on 2023-01-13 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0041_alter_cotacoesdasacoes_nome_da_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='balanco',
            name='nome_da_empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.company'),
        ),
    ]
