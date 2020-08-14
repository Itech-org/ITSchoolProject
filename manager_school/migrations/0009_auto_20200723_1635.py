# Generated by Django 3.0.8 on 2020-07-23 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0008_auto_20200720_1800'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classmodel',
            options={'ordering': ['-date'], 'verbose_name': 'Занятие', 'verbose_name_plural': 'Занятия'},
        ),
        migrations.AlterField(
            model_name='classmodel',
            name='classroom',
            field=models.ManyToManyField(default=None, related_name='classroom', to='manager_school.Classroom'),
        ),
        migrations.CreateModel(
            name='StudyRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enter_date', models.DateTimeField(blank=True, verbose_name='Дата входа')),
                ('first_name', models.CharField(blank=True, max_length=128, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=128, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=128, verbose_name='Отчетсво')),
                ('communication_type', models.CharField(blank=True, max_length=256, verbose_name='Способ связи')),
                ('theses_of_conversation', models.TextField(blank=True, verbose_name='Тезисы разговора')),
                ('source', models.CharField(max_length=256, verbose_name='Источник')),
                ('status', models.CharField(choices=[('R', 'Ready'), ('IP', 'In Progress'), ('D', 'Denial')], max_length=20, verbose_name='Статус лида')),
                ('course', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='manager_school.CourseUser', verbose_name='Курс')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Специалист')),
            ],
            options={
                'verbose_name': 'Лид',
                'verbose_name_plural': 'Лиды',
                'ordering': ['enter_date', 'status', 'last_name'],
            },
        ),
    ]
