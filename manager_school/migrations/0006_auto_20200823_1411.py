# Generated by Django 3.0.8 on 2020-08-23 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_school', '0005_auto_20200822_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeworkmodel',
            name='comment_file',
            field=models.FileField(blank=True, upload_to='file/comment_file/', verbose_name='Файл к комментарию'),
        ),
        migrations.AddField(
            model_name='homeworkmodel',
            name='comment_teacher',
            field=models.TextField(blank=True, verbose_name='Комментарий учителя'),
        ),
        migrations.AlterField(
            model_name='homeworkmodel',
            name='status',
            field=models.CharField(choices=[('Проверено', 'Проверено'), ('Не проверено', 'Не проверено'), ('Не сдано', 'Не сдано')], default='Не проверено', max_length=300),
        ),
        migrations.AlterField(
            model_name='materialtext',
            name='img',
            field=models.ImageField(blank=True, default='images/materials/Rectangle.svg', upload_to='images/materials/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='materialtext',
            name='url',
            field=models.URLField(blank=True, default=None, max_length=100, verbose_name='Ссылка на материалы'),
        ),
        migrations.AlterField(
            model_name='materialvideo',
            name='class_field',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='manager_school.ClassModel', verbose_name='Занятие'),
        ),
        migrations.AlterField(
            model_name='materialvideo',
            name='url',
            field=models.URLField(blank=True, default=None, max_length=100, null=True, verbose_name='Ссылка на материалы'),
        ),
    ]