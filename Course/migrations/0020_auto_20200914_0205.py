# Generated by Django 3.0.4 on 2020-09-13 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0019_auto_20200914_0201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='description_kz',
            new_name='description_kk',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='name_kz',
            new_name='name_kk',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='vimeo_kz',
            new_name='vimeo_kk',
        ),
        migrations.RenameField(
            model_name='lessontasks',
            old_name='ans_a_kz',
            new_name='ans_a_kk',
        ),
        migrations.RenameField(
            model_name='lessontasks',
            old_name='ans_b_kz',
            new_name='ans_b_kk',
        ),
        migrations.RenameField(
            model_name='lessontasks',
            old_name='ans_c_kz',
            new_name='ans_c_kk',
        ),
        migrations.RenameField(
            model_name='lessontasks',
            old_name='ans_d_kz',
            new_name='ans_d_kk',
        ),
        migrations.RenameField(
            model_name='lessontasks',
            old_name='description_kz',
            new_name='description_kk',
        ),
        migrations.RenameField(
            model_name='lessontasks',
            old_name='name_kz',
            new_name='name_kk',
        ),
    ]
