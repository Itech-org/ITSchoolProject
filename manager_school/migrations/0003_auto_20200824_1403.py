# Generated by Django 3.0.8 on 2020-08-24 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0002_auto_20200824_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseuser',
            name='is_online',
        ),
        migrations.AlterField(
            model_name='news',
            name='img',
            field=models.ImageField(blank=True, upload_to='images/itnews', verbose_name='Изображение'),
        ),
    ]