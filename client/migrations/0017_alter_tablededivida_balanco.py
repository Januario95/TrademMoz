# Generated by Django 4.1.4 on 2022-12-21 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0016_alter_balanco_ano'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablededivida',
            name='balanco',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.balanco', unique=True),
        ),
    ]
