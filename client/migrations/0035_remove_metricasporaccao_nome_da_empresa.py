# Generated by Django 4.1.4 on 2022-12-23 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0034_alter_metricasporaccao_nome_da_empresa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metricasporaccao',
            name='nome_da_empresa',
        ),
    ]
