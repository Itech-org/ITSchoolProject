# Generated by Django 3.0.8 on 2020-08-17 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classmodel',
            options={'ordering': ['groups', 'date'], 'verbose_name': 'Занятие', 'verbose_name_plural': 'Занятия'},
        ),
    ]
