# Generated by Django 3.0.8 on 2020-08-19 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0003_auto_20200819_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/news/'),
        ),
    ]
