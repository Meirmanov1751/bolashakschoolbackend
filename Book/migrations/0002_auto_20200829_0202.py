# Generated by Django 3.0.4 on 2020-08-28 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='sale',
            field=models.BooleanField(default=False, verbose_name='Скидка'),
        ),
    ]
