# Generated by Django 4.1.4 on 2022-12-20 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_balanco'),
    ]

    operations = [
        migrations.AddField(
            model_name='balanco',
            name='nome',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
