# Generated by Django 3.2.14 on 2022-07-19 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedaggregator', '0002_feed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]