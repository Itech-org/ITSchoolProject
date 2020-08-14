# Generated by Django 3.0.8 on 2020-07-23 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0009_auto_20200723_1635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studyrequest',
            options={'ordering': ['-enter_date', 'status', 'last_name'], 'verbose_name': 'Лид', 'verbose_name_plural': 'Лиды'},
        ),
        migrations.AlterField(
            model_name='studyrequest',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='manager_school.CourseUser', verbose_name='Курс'),
        ),
        migrations.AlterField(
            model_name='studyrequest',
            name='source',
            field=models.CharField(blank=True, max_length=256, verbose_name='Источник'),
        ),
        migrations.AlterField(
            model_name='studyrequest',
            name='specialist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Специалист'),
        ),
        migrations.AlterField(
            model_name='studyrequest',
            name='status',
            field=models.CharField(blank=True, choices=[('Ready', 'Ready'), ('In Progress', 'In Progress'), ('Denial', 'Denial')], max_length=20, verbose_name='Статус лида'),
        ),
    ]