# Generated by Django 3.2.15 on 2022-08-12 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedaggregator', '0015_alter_subscription_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254)),
                ('body', models.TextField()),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedaggregator.feed')),
            ],
        ),
    ]
