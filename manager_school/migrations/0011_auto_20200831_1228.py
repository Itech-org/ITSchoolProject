# Generated by Django 3.0.8 on 2020-08-31 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0010_contactadmin_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactadmin',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('In progress', 'In progress'), ('Waiting', 'Waiting')], default='Waiting', max_length=20, verbose_name='Статус заявки'),
        ),
    ]
