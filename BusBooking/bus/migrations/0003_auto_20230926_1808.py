# Generated by Django 3.2 on 2023-09-26 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0002_auto_20230926_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bustrip',
            name='bus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.businfo'),
        ),
        migrations.AlterField(
            model_name='bustrip',
            name='day',
            field=models.CharField(choices=[('MONDAY', 'MONDAY'), ('TUESDAY', 'TUESDAY'), ('WEDNESDAY', 'WEDNESDAY'), ('THURSDAY', 'THURSDAY'), ('FRIDAY', 'FRIDAY'), ('SATURDAY', 'SATURDAY'), ('SUNDAY', 'SUNDAY')], max_length=500),
        ),
        migrations.AlterField(
            model_name='lugaggeprice',
            name='weight',
            field=models.CharField(choices=[('-15KG', '-15KG'), ('+15KG', '+15KG'), ('+30KG', '+30KG'), ('+50KG', '+50KG')], max_length=500),
        ),
    ]
