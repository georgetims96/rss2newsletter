# Generated by Django 3.2.15 on 2022-09-15 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedaggregator', '0020_alter_entry_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name_plural': 'entries'},
        ),
    ]
