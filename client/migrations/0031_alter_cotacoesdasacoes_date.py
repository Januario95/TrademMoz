# Generated by Django 4.1.4 on 2022-12-23 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0030_alter_cotacoesdasacoes_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotacoesdasacoes',
            name='date',
            field=models.DateField(blank=True),
        ),
    ]
