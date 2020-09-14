# Generated by Django 3.0.4 on 2020-08-28 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0009_moduleuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduleuser',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='LessonUserHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(default=0)),
                ('last_visited', models.DateTimeField(auto_now=True, null=True)),
                ('visited_count', models.IntegerField(default=0)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.Lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.Module')),
            ],
        ),
    ]