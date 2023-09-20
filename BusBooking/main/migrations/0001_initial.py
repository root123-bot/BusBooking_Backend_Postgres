# Generated by Django 3.2 on 2023-09-20 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceAuthModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelId', models.CharField(max_length=255)),
                ('pin', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceNotificationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceNotificationToken', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notificationToken', to='register.customuser')),
            ],
        ),
    ]
