# Generated by Django 4.1.4 on 2022-12-30 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0040_alter_company_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotacoesdasacoes',
            name='nome_da_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.company'),
        ),
    ]
