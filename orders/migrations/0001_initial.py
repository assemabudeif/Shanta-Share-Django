# Generated by Django 5.1.1 on 2024-09-19 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0008_alter_client_profile_picture_and_more'),
        ('posts', '0005_alter_post_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=16)),
                ('payment_status', models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid', max_length=16)),
                ('client_notes', models.CharField(max_length=255)),
                ('pickup_time', models.DateTimeField(null=True)),
                ('arrival_time', models.DateTimeField(null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='useer_orders', to='authentication.client')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='orders', to='posts.post')),
            ],
        ),
    ]
