# Generated by Django 3.2 on 2023-10-01 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0012_alter_bookedseat_booked_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busseatlayout',
            name='bus',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seatmetadata', to='bus.businfo'),
        ),
    ]
