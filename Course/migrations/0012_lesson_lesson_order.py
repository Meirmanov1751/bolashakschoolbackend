# Generated by Django 3.0.4 on 2020-08-28 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0011_auto_20200828_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_order',
            field=models.IntegerField(default=0, verbose_name='Позиция урока'),
        ),
    ]
