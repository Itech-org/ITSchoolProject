# Generated by Django 3.0.8 on 2020-08-20 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0003_homeworkteachermodel_attempts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homeworkmodel',
            name='slug',
        ),
    ]