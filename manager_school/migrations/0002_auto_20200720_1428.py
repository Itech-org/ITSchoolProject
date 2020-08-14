# Generated by Django 3.0.8 on 2020-07-20 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Material',
            new_name='MaterialText',
        ),
        migrations.AlterModelOptions(
            name='materialtext',
            options={'verbose_name': 'Тесктовый материал', 'verbose_name_plural': 'Текстовые материалы'},
        ),
        migrations.AlterField(
            model_name='homeworkmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_st', to=settings.AUTH_USER_MODEL, verbose_name='Студент'),
        ),
        migrations.CreateModel(
            name='MaterialVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, max_length=700, verbose_name='Описание материала')),
                ('url', models.URLField(max_length=100, verbose_name='Ссылка на материалы')),
                ('slug', models.SlugField(default=None, max_length=100)),
                ('class_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_school.ClassModel', verbose_name='Занятие')),
            ],
            options={
                'verbose_name': 'Тесктовый виделматериал',
                'verbose_name_plural': 'Текстовые видеоматериалы',
            },
        ),
    ]
