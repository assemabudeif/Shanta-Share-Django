# Generated by Django 5.1.1 on 2024-09-14 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='from_address_line',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='to_address_line',
            field=models.TextField(null=True),
        ),
    ]
