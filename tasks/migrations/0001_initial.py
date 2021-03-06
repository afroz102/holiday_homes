# Generated by Django 3.1.7 on 2021-04-13 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_auto_20210408_1124'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('units', '0002_remove_unit_status'),
        ('bookings', '0014_auto_20210413_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_details', models.TextField(blank=True)),
                ('task_date', models.DateField(null=True)),
                ('task_time', models.TimeField(null=True)),
                ('task_status', models.CharField(choices=[('status_1', 'PENDING'), ('status_2', 'IN PROGRESS'), ('status_3', 'COMPLETED'), ('status_4', 'CANCELED')], default='PENDING', max_length=250)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bookings.booking')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.usercompany')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='units.unit')),
            ],
        ),
        migrations.CreateModel(
            name='TaskManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.userprofile')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
            ],
        ),
    ]
