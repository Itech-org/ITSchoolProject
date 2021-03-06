# Generated by Django 3.0.8 on 2020-08-31 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0002_auto_20200824_1323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseuser',
            old_name='discription',
            new_name='description',
        ),
        migrations.AddField(
            model_name='chat',
            name='chat_title',
            field=models.CharField(max_length=100, null=True, verbose_name='Название чата'),
        ),
        migrations.AlterField(
            model_name='classmodel',
            name='room_link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на комнату занятия'),
        ),
    ]
