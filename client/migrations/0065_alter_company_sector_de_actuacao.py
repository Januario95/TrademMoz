# Generated by Django 4.1.4 on 2023-01-30 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0064_company_sector_de_actuacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='sector_de_actuacao',
            field=models.CharField(choices=[('bebidas', 'Bebidas'), ('seguros', 'Seguros'), ('servicos', 'Servicos'), ('energia-hidroelectrica', 'Energia Hidroelectrica'), ('portagem', 'Portagem')], default='bebidas', max_length=100),
        ),
    ]