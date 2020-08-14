# Generated by Django 3.0.8 on 2020-07-24 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0010_auto_20200723_1728'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classmodel',
            options={'ordering': ['date'], 'verbose_name': 'Занятие', 'verbose_name_plural': 'Занятия'},
        ),
        migrations.RemoveField(
            model_name='studyrequest',
            name='theses_of_conversation',
        ),
        migrations.CreateModel(
            name='RequestConversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, verbose_name='Дата разговора')),
                ('theses_of_conversation', models.TextField(blank=True, verbose_name='Тезисы разговора')),
                ('status', models.CharField(blank=True, choices=[('Ready', 'Ready'), ('In Progress', 'In Progress'), ('Denial', 'Denial')], max_length=20, verbose_name='Статус лида')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_school.StudyRequest', verbose_name='Заявка')),
            ],
            options={
                'verbose_name': 'Разговор',
                'verbose_name_plural': 'Разговоры',
                'ordering': ['date', 'status'],
            },
        ),
    ]