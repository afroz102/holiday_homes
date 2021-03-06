# Generated by Django 3.1.7 on 2021-04-10 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookings', '0005_auto_20210410_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingnote',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='guest',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='guest',
            name='document_type',
            field=models.CharField(blank=True, choices=[('Passport', 'Passport'), ('Emirates Id', 'Emirates Id'), ('Other', 'Other')], max_length=250),
        ),
        migrations.AlterField(
            model_name='mainguestbookingmapping',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
