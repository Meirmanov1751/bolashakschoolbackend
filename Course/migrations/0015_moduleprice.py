# Generated by Django 3.0.4 on 2020-09-01 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0014_auto_20200901_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModulePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('module', models.ManyToManyField(to='Course.Module')),
            ],
        ),
    ]