# Generated by Django 5.1.1 on 2024-09-19 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_cargo_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cargo_images',
        ),
        migrations.AddField(
            model_name='order',
            name='cargo_image',
            field=models.ImageField(blank=True, upload_to='cargo_images'),
        ),
    ]
