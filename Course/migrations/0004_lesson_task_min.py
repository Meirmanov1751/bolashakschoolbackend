# Generated by Django 3.0.4 on 2020-08-27 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0003_auto_20200827_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='task_min',
            field=models.IntegerField(null=True, verbose_name='Минимум для прохода'),
        ),
    ]
