# Generated by Django 3.0.8 on 2020-08-23 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0006_auto_20200823_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeworkmodel',
            name='rating',
            field=models.PositiveIntegerField(blank=True, verbose_name='Оценка'),
        ),
    ]