# Generated by Django 3.0.4 on 2020-08-27 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0005_lesson_free'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessontasks',
            name='correct',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=2, verbose_name='Правильный ответ'),
        ),
    ]
