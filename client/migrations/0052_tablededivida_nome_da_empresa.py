# Generated by Django 4.1.4 on 2023-01-19 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0051_alter_metricasporaccao_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablededivida',
            name='nome_da_empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.company'),
        ),
    ]