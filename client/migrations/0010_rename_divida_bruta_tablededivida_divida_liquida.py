# Generated by Django 4.1.4 on 2022-12-20 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_alter_balanco_activo_corrente_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tablededivida',
            old_name='divida_bruta',
            new_name='divida_liquida',
        ),
    ]