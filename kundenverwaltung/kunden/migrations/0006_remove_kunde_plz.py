# Generated by Django 5.1.7 on 2025-03-17 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kunden', '0005_kunde_plz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kunde',
            name='plz',
        ),
    ]
