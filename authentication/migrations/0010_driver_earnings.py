# Generated by Django 5.1.1 on 2024-09-24 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_alter_baseuser_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='earnings',
            field=models.FloatField(default=0.0),
        ),
    ]
