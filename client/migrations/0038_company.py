# Generated by Django 4.1.4 on 2022-12-30 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0037_alter_tablededivida_balanco'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='CDM', max_length=125)),
            ],
        ),
    ]