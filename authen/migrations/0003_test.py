# Generated by Django 5.1.1 on 2024-09-11 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authen', '0002_car_carimage_carlicense_clientphonenumber_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
    ]
