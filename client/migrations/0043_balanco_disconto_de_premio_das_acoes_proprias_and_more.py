# Generated by Django 4.1.4 on 2023-01-16 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0042_balanco_nome_da_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='balanco',
            name='disconto_de_premio_das_acoes_proprias',
            field=models.DecimalField(decimal_places=2, default=-1.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='balanco',
            name='resultados_de_exercicio',
            field=models.DecimalField(decimal_places=2, default=-1.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='balanco',
            name='resultados_transitado',
            field=models.DecimalField(decimal_places=2, default=-1.0, max_digits=20),
        ),
    ]
