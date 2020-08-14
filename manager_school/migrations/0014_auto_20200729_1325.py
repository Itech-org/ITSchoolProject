# Generated by Django 3.0.8 on 2020-07-29 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0013_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classmodel',
            name='classroom',
        ),
        migrations.AddField(
            model_name='classmodel',
            name='classroom',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classroom', to='manager_school.Classroom'),
        ),
        migrations.AlterField(
            model_name='classmodel',
            name='groups',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='manager_school.GroupModel', verbose_name='Группа'),
        ),
    ]