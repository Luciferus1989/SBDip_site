# Generated by Django 5.0 on 2023-12-19 01:27

import shopapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to=shopapp.models.product_preview_directory_path),
        ),
    ]