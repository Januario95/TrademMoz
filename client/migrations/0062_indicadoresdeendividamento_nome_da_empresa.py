# Generated by Django 4.1.4 on 2023-01-24 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0061_indicadoresdecrescimento_nome_da_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicadoresdeendividamento',
            name='nome_da_empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.company'),
        ),
    ]
