# Generated by Django 5.1.1 on 2024-09-18 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_rename_city_id_client_city_ids_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='profile_picture',
            field=models.ImageField(default='null', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='driver',
            name='profile_picture',
            field=models.ImageField(default='null', upload_to=''),
            preserve_default=False,
        ),
    ]
