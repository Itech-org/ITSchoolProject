# Generated by Django 3.0.8 on 2020-08-18 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0036_auto_20200813_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='RubruckNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, verbose_name='Рубрика')),
            ],
            options={
                'verbose_name': 'Рубрика',
                'verbose_name_plural': 'Рубрики',
            },
        ),
        migrations.AddField(
            model_name='news',
            name='rubrick',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='manager_school.RubruckNews'),
        ),
    ]