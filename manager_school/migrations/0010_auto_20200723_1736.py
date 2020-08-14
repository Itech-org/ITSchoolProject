# Generated by Django 3.0.8 on 2020-07-23 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0009_auto_20200723_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialtext',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание материала'),
        ),
        migrations.AlterField(
            model_name='materialvideo',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание материала'),
        ),
        migrations.AlterField(
            model_name='materialvideo',
            name='file',
            field=models.FileField(blank=True, upload_to='file/video_materials/', verbose_name='Файл'),
        ),
    ]