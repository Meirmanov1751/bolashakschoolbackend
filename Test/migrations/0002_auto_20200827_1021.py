# Generated by Django 3.0.4 on 2020-08-27 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testgroupcategory',
            name='test_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_group_categories', to='Test.TestGroup', verbose_name='Тест'),
        ),
    ]
