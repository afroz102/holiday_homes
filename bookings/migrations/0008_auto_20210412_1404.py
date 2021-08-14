# Generated by Django 3.1.7 on 2021-04-12 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210408_1124'),
        ('bookings', '0007_reorderstringlogic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reorderstringlogic',
            name='booking',
        ),
        migrations.AddField(
            model_name='reorderstringlogic',
            name='company',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.usercompany'),
        ),
    ]