# Generated by Django 5.1.1 on 2024-09-14 14:31

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('review_text', models.TextField()),
                ('review_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='authentication.client')),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.driver')),
            ],
        ),
    ]
