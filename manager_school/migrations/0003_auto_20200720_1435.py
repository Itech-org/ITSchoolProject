# Generated by Django 3.0.8 on 2020-07-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0002_auto_20200720_1428'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='materialvideo',
            options={'verbose_name': 'Видеоматериал', 'verbose_name_plural': 'Видеоматериалы'},
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='classes',
        ),
        migrations.AddField(
            model_name='classmodel',
            name='classes',
            field=models.ManyToManyField(to='manager_school.ClassModel'),
        ),
    ]