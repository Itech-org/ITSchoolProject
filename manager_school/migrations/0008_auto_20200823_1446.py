# Generated by Django 3.0.8 on 2020-08-23 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0007_auto_20200823_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeworkmodel',
            name='status',
            field=models.CharField(choices=[('g', 'Проверено'), ('nv', 'Не проверено'), ('n', 'Не сдано')], default='n', max_length=300),
        ),
    ]