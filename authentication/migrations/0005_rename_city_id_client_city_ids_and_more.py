# Generated by Django 5.1.1 on 2024-09-14 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_client_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='city_id',
            new_name='city_ids',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='phone_number',
            new_name='phone_numbers',
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='car_id',
            new_name='car_ids',
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='city_id',
            new_name='city_ids',
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='driver_license_id',
            new_name='driver_license_ids',
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='phone_number',
            new_name='phone_numbers',
        ),
    ]
