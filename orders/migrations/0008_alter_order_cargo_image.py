# Generated by Django 5.1.1 on 2024-09-21 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_remove_order_cargo_images_order_cargo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cargo_image',
            field=models.ImageField(blank=True, null=True, upload_to='cargo_images'),
        ),
    ]
