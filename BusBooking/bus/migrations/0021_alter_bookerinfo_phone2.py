# Generated by Django 3.2 on 2023-12-19 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0020_auto_20231219_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookerinfo',
            name='phone2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]