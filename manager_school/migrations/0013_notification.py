# Generated by Django 3.0.8 on 2020-07-29 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0012_auto_20200724_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('recieved_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата получения')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_school.GroupModel', verbose_name='Получатель')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender_notification', to='manager_school.ClassModel', verbose_name='Отправитель')),
            ],
            options={
                'verbose_name': 'Уведомление о изменении ',
                'verbose_name_plural': 'Уведомления о изменениях',
            },
        ),
    ]
