# Generated by Django 3.2 on 2024-01-06 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
