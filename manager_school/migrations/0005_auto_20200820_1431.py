# Generated by Django 3.0.8 on 2020-08-20 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0004_remove_homeworkmodel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeworkmodel',
            name='status',
            field=models.CharField(choices=[('Проверено', 'Проверено'), ('Не проверено', 'Не проверено'), ('Не сдано', 'Не сдано')], default='Не проверено', max_length=300),
        ),
    ]