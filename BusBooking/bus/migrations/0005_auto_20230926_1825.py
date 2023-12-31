# Generated by Django 3.2 on 2023-09-26 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0004_auto_20230926_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bustrip',
            name='bus_arrival_time',
        ),
        migrations.RemoveField(
            model_name='bustrip',
            name='duration',
        ),
        migrations.AddField(
            model_name='bustrip',
            name='destination_arrival_time',
            field=models.CharField(default='17:30', help_text='eg. 17:30, put format in 24 hours, muda wa basi kufika kituo cha mwisho cha safari', max_length=500),
        ),
        migrations.AddField(
            model_name='bustrip',
            name='source_arrival_time',
            field=models.CharField(default='17:30', help_text='eg. 17:30, put format in 24 hours, muda wa basi kufika kituo cha kuanza safari', max_length=500),
        ),
        migrations.AlterField(
            model_name='bustrip',
            name='bus_departure_time',
            field=models.CharField(help_text='eg. 18:00, put format in 24 hours, muda wa basi kuondoka kuanza safari', max_length=500),
        ),
    ]
