# Generated by Django 5.0 on 2023-12-19 03:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='item',
        ),
        migrations.AddField(
            model_name='feedback',
            name='item',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='shopapp.item'),
            preserve_default=False,
        ),
    ]
