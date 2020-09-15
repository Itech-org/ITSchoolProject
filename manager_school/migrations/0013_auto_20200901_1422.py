# Generated by Django 3.0.8 on 2020-09-01 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0012_merge_20200901_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classmodel',
            name='room_link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на комнату занятия'),
        ),
        migrations.AlterField(
            model_name='homeworkmodel',
            name='description',
            field=models.TextField(blank=True, max_length=512, verbose_name='Описание ДЗ'),
        ),
        migrations.AlterField(
            model_name='homeworkteachermodel',
            name='description',
            field=models.TextField(blank=True, max_length=512, verbose_name='Описание ДЗ'),
        ),
        migrations.AlterField(
            model_name='news',
            name='img',
            field=models.ImageField(blank=True, upload_to='images/itnews', verbose_name='Изображение'),
        ),
        migrations.CreateModel(
            name='PersonalNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=512, verbose_name='Текст уведомления')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Время получения')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Персональное уведомление',
                'verbose_name_plural': 'Персональные уведомления',
            },
        ),
    ]