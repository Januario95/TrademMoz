# Generated by Django 4.1.4 on 2022-12-20 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_alter_tablededivida_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemonstracaoDeResultados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendas', models.DecimalField(decimal_places=2, max_digits=20)),
                ('lucros_bruto', models.DecimalField(decimal_places=2, max_digits=20)),
                ('EBITIDA', models.DecimalField(blank=True, decimal_places=2, max_digits=20)),
                ('EBIT', models.DecimalField(decimal_places=2, max_digits=20)),
                ('lucro_antes_de_imposto', models.DecimalField(decimal_places=2, max_digits=20)),
                ('lucro_liquido_depois_de_imposto', models.DecimalField(decimal_places=2, max_digits=20)),
                ('dividendo_declarados_e_pagos', models.DecimalField(decimal_places=2, max_digits=20)),
                ('numero_medio_ponderado_de_acoes', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
            options={
                'verbose_name': 'Demonstracao De Resultados',
                'verbose_name_plural': 'Demonstracao De Resultados',
            },
        ),
        migrations.AlterModelOptions(
            name='balanco',
            options={'verbose_name': 'Balanco', 'verbose_name_plural': 'Balancos'},
        ),
    ]