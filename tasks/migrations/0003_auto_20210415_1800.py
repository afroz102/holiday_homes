# Generated by Django 3.1.7 on 2021-04-15 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20210415_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
