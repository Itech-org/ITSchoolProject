# Generated by Django 3.0.8 on 2020-09-05 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0005_auto_20200904_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomTimeInterval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_from', models.TimeField(verbose_name='')),
                ('time_to', models.TimeField(verbose_name='')),
                ('is_free', models.BooleanField(default=True, verbose_name='')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_intervals', to='manager_school.Classroom', verbose_name='')),
            ],
            options={
                'verbose_name': 'Временной промежуток занятости аудитории',
                'verbose_name_plural': 'Временные промежутки занятости аудитории',
            },
        ),
    ]
