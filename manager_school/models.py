import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
from .utilities import slugify
from time import time
# Create your models here.


def gen_slug(s):
    new_slug = slugify(s)
    return new_slug + '-' + str(int(time()))


class AdvUser(AbstractUser): # Студенты
    surname = models.CharField(max_length=30 ,db_index=True, verbose_name="Отчество", blank=True)
    img_user = models.ImageField('Аватар', upload_to='images/user/', blank=True)
    phone = models.CharField(max_length=30 , verbose_name="Номер телефона", blank=True)

    def get_academic_performance(self, group_id=''):
        if self.groups.filter(name="Student").exists():
            academic_performance = 0
            if group_id == '':
                attendances = self.attendances.all()
                attendances_true = self.attendances.filter(attendance=True)
                homework = self.homework_st.filter(status='Проверено')
            else:
                attendances = self.attendances.filter(classes__groups__id=group_id)
                attendances_true = self.attendances.filter(attendance=True, classes__groups__id=group_id)
                homework = self.homework_st.filter(status='Проверено', class_field__groups__id=group_id)
            if attendances_true:
                for attendance in attendances_true:
                    academic_performance += attendance.rating
            if homework:
                for hw in homework:
                    academic_performance += hw.rating
            try:
                return int(academic_performance / (len(attendances)+len(homework))) * 10
            except ZeroDivisionError:
                return 0
        return 0

    def get_attendance(self, group_id=''):
        if self.groups.filter(name="Student").exists():
            current_day = datetime.date.today()
            if group_id == '':
                attendances = self.attendances.all()
                classes = ClassModel.objects.filter(groups__students__id=self.id, date__lt=current_day)
            else:
                attendances = self.attendances.filter(classes__groups__id=group_id)
                classes = ClassModel.objects.filter(
                    groups__students__id=self.id, groups__id=group_id, date__gt=current_day)
            try:
                attendance = len(attendances.filter(attendance=True)) / len(classes) * 100
            except ZeroDivisionError:
                attendance = 0
            return attendance
        return 0

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.surname}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserManagement(models.Model):
    student = models.OneToOneField(AdvUser, on_delete=models.SET_NULL, null=True, verbose_name="Студент", related_name="management")
    manager = models.ForeignKey(AdvUser, on_delete=models.SET_NULL, null=True, verbose_name="Менеджер", related_name="user_management")

    class Meta:
        verbose_name = 'Привязка к менеджеру'
        verbose_name_plural = 'Привязки к менеджерам'


class CourseUser(models.Model):  # Курс
    title = models.CharField(max_length=150, db_index=True, verbose_name='Название', blank=True)
    discription = models.TextField('Описание', blank=True)
    price = models.FloatField(verbose_name='Цена', default =0)
    start_date = models.DateField(verbose_name='Начало занятий', null=True)
    finish_date = models.DateField(verbose_name='Конец занятий', null=True)
    img = models.ImageField(upload_to='images/courses/', verbose_name='Логотип курса')
    amount = models.CharField(max_length=50, db_index=True, verbose_name='Количество занятий')
    slug = models.SlugField(max_length=100, db_index=True, default=None)
    is_online = models.BooleanField(default=False, verbose_name="Онлайн?")
    def __str__(self):
        return f"{self.title}"

    def get_obj(self):
        return self.id, self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class GroupModel(models.Model):     # Группа
    students = models.ManyToManyField(AdvUser)
    teacher = models.ForeignKey(AdvUser, verbose_name='Учитель', on_delete=models.PROTECT, related_name='groups_teacher', default=None, null=True)
    manager = models.ForeignKey(AdvUser, verbose_name='Куратор', on_delete=models.PROTECT, related_name='groups_manager', default=None, null=True)
    course = models.ForeignKey(CourseUser, verbose_name='Курс', on_delete=models.CASCADE, related_name='groups', default=None, null=True)
    title = models.CharField('Название', max_length=100, blank=True)
    slug = models.SlugField(max_length=100, db_index=True, default=None, null=True)

    def get_academic_performance(self):
        attendances = Attendance.objects.filter(classes__groups__id=self.id)
        attendances_count = len(attendances)
        performance = 0
        if attendances:
            for attendance in attendances:
                if attendance.rating:
                    performance += attendance.rating
                else:
                    attendances_count -= 1
            return round(performance / attendances_count, 2)
        else:
             return 0.0

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class ClassModel(models.Model):  # Занятие
    groups = models.ForeignKey(GroupModel, verbose_name='Группа', on_delete=models.CASCADE, related_name='classes',
                               default=None, null=True)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE, default=None, related_name='classroom',
                                  null=True)
    date = models.DateField(null=True, verbose_name='Дата проведения занятия')
    start_time = models.TimeField(null=True, verbose_name='Время начала занятия')
    end_time = models.TimeField(null=True, verbose_name='Время окончания занятия')
    theme = models.CharField(max_length=250, verbose_name='Тема', blank=True)
    file = models.FileField(upload_to='file/video_course/', verbose_name='Файл с видео', blank=True)
    slug = models.SlugField(max_length=100, db_index=True, default=None, blank=True)
    position = models.IntegerField(default=1, null=True, verbose_name="Номер занятия")
    room_link = models.URLField(null=True, blank=True, verbose_name="Ссылка на комнату занятия")
    message = models.TextField(verbose_name='Сообщение', blank=True)


    def __str__(self):
        return self.theme

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.theme)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['groups', 'date']
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'


class Attendance(models.Model): #Посещение
    classes =models.ForeignKey(ClassModel, on_delete=models.CASCADE, related_name='attendances')
    students = models.ForeignKey(AdvUser, on_delete=models.CASCADE, related_name="attendances")
    rating = models.IntegerField('Оценка', null=True, blank=True)
    attendance = models.BooleanField('Присутствие', default=False)

    class Meta:
        ordering = ['students', 'attendance', 'rating',]
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'


class Notification(models.Model): #уведомление для группы
    sender = models.ForeignKey(ClassModel, on_delete=models.CASCADE, null=True, related_name='sender_notification',
                               verbose_name='Отправитель')
    recipient = models.ForeignKey(GroupModel, on_delete=models.CASCADE, verbose_name='Получатель')
    message = models.TextField(verbose_name='Сообщение')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения')

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Уведомление о изменении '
        verbose_name_plural = 'Уведомления о изменениях'


class PersonalNotification(models.Model): #персональные уведомления
    recipient = models.ForeignKey(AdvUser, verbose_name='Получатель', on_delete=models.CASCADE)
    message = models.TextField(max_length=512, verbose_name='Текст уведомления')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Время получения')

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Персональное уведомление'
        verbose_name_plural = 'Персональные уведомления'


class Classroom(models.Model): #Аудитория
    title = models.CharField('Аудитория', max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'


class HomeworkModel(models.Model):  # Дз Студента
    CHOICES = (
        ('Проверено', 'Проверено'),
        ('Не проверено', 'Не проверено'),
        ('Не сдано', 'Не сдано'),
        )

    title = models.CharField(max_length=150, db_index=True, verbose_name='Название', blank=True)
    file = models.FileField(upload_to='file/student/', verbose_name='Файл с ДЗ', blank=True)
    description = models.TextField(max_length=512, verbose_name='Описание ДЗ', blank=True)
    url = models.URLField(max_length=100, verbose_name='Ссылка дз', blank=True, null=True, default=None)
    class_field = models.ForeignKey(ClassModel, verbose_name='Занятие', on_delete=models.CASCADE, related_name='homework', null=True, default=None)
    user = models.ForeignKey(AdvUser, verbose_name='Студент', on_delete=models.CASCADE, related_name='homework_st')
    status = models.CharField(max_length=300, choices = CHOICES, default='Не проверено')
    rating = models.PositiveIntegerField('Оценка', blank=True)
    comment_teacher = models.TextField('Комментарий учителя', blank=True)
    comment_file = models.FileField('Файл к комментарию', upload_to='file/comment_file/', blank=True)

    def __str__(self):
        return f" {self.title}"

    class Meta:
        verbose_name = 'ДЗ Студена'
        verbose_name_plural = 'ДЗ Студентов'


class HomeworkTeacherModel(models.Model): # Дз Препода
    title = models.CharField(max_length=150, db_index=True, verbose_name='Название')
    file = models.FileField(upload_to='file/teacher/', verbose_name='Файл с ДЗ', blank=True)
    description = models.TextField(max_length=512, verbose_name='Описание ДЗ', blank=True)
    url = models.URLField(max_length=100, verbose_name='Ссылка дз', null=True, blank=True)
    class_field = models.ForeignKey(ClassModel, verbose_name='Занятие', on_delete=models.CASCADE, related_name='homeworkteacher')
    attempts = models.IntegerField(verbose_name='Количество попыток', default=3)
    slug = models.SlugField(max_length=100, db_index=True, default=None)

    def __str__(self):
        return f" {self.title}"

    class Meta:
        verbose_name = 'ДЗ Преподавателя'
        verbose_name_plural = 'ДЗ Преподавателей'


class MaterialText(models.Model): #Материалы
    title = models.CharField(max_length=250, verbose_name='Заголовок', blank=True)
    img = models.ImageField(default='images/materials/Rectangle.svg', upload_to='images/materials/',
                            verbose_name='Изображение', blank=True)
    description = models.TextField('Описание материала', blank=True)
    url = models.URLField(max_length=100, verbose_name='Ссылка на материалы',  blank=True, default=None)
    class_field = models.ForeignKey(ClassModel, verbose_name='Занятие', on_delete=models.CASCADE, null=True, default=None, blank=True)
    file = models.FileField(upload_to='file/text_materials/', verbose_name='Файл', blank=True)
    slug = models.SlugField(max_length=100, db_index=True, default=None)

    def __str__(self):
        return f" {self.title}"

    class Meta:
        verbose_name = 'Тесктовый материал'
        verbose_name_plural = 'Текстовые материалы'


class MaterialVideo(models.Model): #Материалы
    title = models.CharField(max_length=250, verbose_name='Заголовок', blank=True)
    description = models.TextField('Описание материала', blank=True)
    url = models.URLField(max_length=100, verbose_name='Ссылка на материалы', null=True, default=None, blank=True)
    class_field = models.ForeignKey(ClassModel, verbose_name='Занятие', on_delete=models.CASCADE, null=True, default=None, blank=True)
    file = models.FileField(upload_to='file/video_materials/', verbose_name='Файл', blank=True)
    slug = models.SlugField(max_length=100, db_index=True, default=None)

    def __str__(self):
        return f" {self.title}"

    class Meta:
        verbose_name = 'Видеоматериал'
        verbose_name_plural = 'Видеоматериалы'


class RubruckNews(models.Model):
    title = models.CharField("Рубрика", max_length=30, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'


class News(models.Model):
    img = models.ImageField('Изображение', upload_to='images/itnews', blank=True)
    title = models.CharField('Заголовок', max_length=150, blank=True)
    description = models.TextField('Тело', blank = True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.SlugField(max_length=200, db_index=True, blank=True)
    rubrick = models.ForeignKey(RubruckNews, on_delete=models.CASCADE, null=True, default=None)
    picture = models.ImageField(upload_to='images/news/', null=True, blank=True)

    def __str__(self):
        return f" {self.title}"

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class StudyRequest(models.Model):
    CHOICES = (
        ('Ready', 'Ready'),
        ('In Progress', 'In Progress'),
        ('Denial', 'Denial'),
    )
    enter_date = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Дата входа", blank=True)
    first_name = models.CharField(max_length=128, verbose_name="Имя", blank=True)
    last_name = models.CharField(max_length=128, verbose_name="Фамилия", blank=True)
    patronymic = models.CharField(max_length=128, verbose_name="Отчетсво", blank=True)
    communication_type = models.CharField(max_length=256, verbose_name="Способ связи", blank=True)
    tel_number = models.CharField(max_length=20, verbose_name="Телефон", null=True, blank=True)
    email = models.EmailField(verbose_name="E-mail", null=True, blank=True)
    course = models.ForeignKey(CourseUser, on_delete=models.PROTECT, verbose_name="Курс", blank=True, null=True)
    source = models.CharField(max_length=256, verbose_name="Источник", blank=True)
    specialist = models.ForeignKey(AdvUser, on_delete=models.PROTECT, verbose_name="Специалист", blank=True, null=True)
    status = models.CharField(max_length=20, choices=CHOICES, verbose_name="Статус лида", blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        ordering = ['-enter_date', 'status', 'last_name']
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'


class RequestConversation(models.Model):
    CHOICES = (
        ('Ready', 'Ready'),
        ('Сall back', 'Сall back'),
        ('Denial', 'Denial'),
    )
    request = models.ForeignKey(StudyRequest, on_delete=models.CASCADE, verbose_name="Заявка")
    date = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Дата разговора", null=True, blank=True)
    theses_of_conversation = models.TextField(verbose_name="Тезисы разговора", blank=True)
    status = models.CharField(max_length=20, choices=CHOICES, verbose_name="Статус лида", null=True, blank=True)

    def __str__(self):
        return f"#{self.request.id} | {self.request} - {self.status}"

    class Meta:
        ordering = ['-date', 'status']
        verbose_name = 'Разговор'
        verbose_name_plural = 'Разговоры'


class Contract(models.Model):
    lead = models.OneToOneField(StudyRequest, on_delete=models.PROTECT, verbose_name="Лид", related_name="contract", null=True)
    number = models.CharField(max_length=126, verbose_name="Номер договора", unique=True)
    date = models.DateField(verbose_name="Дата заключения договора")
    course = models.ForeignKey(CourseUser, on_delete=models.PROTECT, verbose_name="Курс", null=True)
    group = models.ForeignKey(GroupModel, on_delete=models.PROTECT, verbose_name="Группа", null=True)
    account = models.ForeignKey(AdvUser, on_delete=models.PROTECT, verbose_name="Аккаунт", null=True)
    price = models.FloatField(verbose_name='Цена', null=True)
    is_subscribed = models.BooleanField(default=False, verbose_name="Контракт подписан?")

    def __str__(self):
        return f"#{self.number} | {self.course} - {self.group}"

    class Meta:
        ordering = ['-date', '-price']
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'


class UserPayment(models.Model):
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, verbose_name="Договор", related_name="payment")
    by_stages = models.BooleanField(default=False, verbose_name="Разбить на этапы?")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")

    def __str__(self):
        return f"{self.id} | {self.contract}"

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class PaymentStage(models.Model):
    picture = models.ImageField(upload_to='images/user/', verbose_name="Чек", null=True, blank=True)
    price = models.FloatField(verbose_name='Цена', null=True)
    date = models.DateField(verbose_name="Дата платежа")
    payment = models.ForeignKey(UserPayment, on_delete=models.CASCADE, verbose_name="Оплата")
    is_confirmed = models.BooleanField(default=False, verbose_name="Подтвержден?")

    def __str__(self):
        return f"{self.payment} - {self.price} | {self.date}"

    class Meta:
        ordering = ['date']
        verbose_name = 'Этап оплата'
        verbose_name_plural = 'Этапы оплаты'


class ChatManager(models.Manager):
    """Модель менеджера чатов"""
    use_for_related_fields = True

    def unreaded(self, user=None):
        qs = self.get_queryset().exclude(last_message__isnull=True).filter(last_message__is_readed=False)
        return qs.exclude(last_message__author=user) if user else qs


class Chat(models.Model):
    """Модель чата"""

    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, 'Dialog'),
        (CHAT, 'Chat')
    )

    type = models.CharField(
        'Тип',
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(AdvUser, verbose_name="Участники")
    last_message = models.ForeignKey('Message', related_name='last_message', null=True, blank=True,
                                     on_delete=models.SET_NULL)
    objects = ChatManager()

    def get_absolute_url(self):
        return reverse('manager_school:messages', args=[self.pk])

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    """Модель сообщения в чате"""

    chat = models.ForeignKey(Chat, verbose_name="Чат", on_delete=models.CASCADE)
    author = models.ForeignKey(AdvUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    message = RichTextUploadingField(null=True, blank=True, config_name='message_config')
    pub_date = models.DateTimeField('Дата сообщения', default=timezone.now)
    is_readed = models.BooleanField('Прочитано', default=False)
    document = models.FileField(upload_to='file/chat_document/', verbose_name='Файл', blank=True)

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.message


class Costs(models.Model): # Расходы
    date = models.DateTimeField(null=True, verbose_name='Дата')
    breakdown = models.TextField('Поломки', blank=True)
    chancery = models.TextField('Канцелярия', blank=True)
    grocery = models.TextField('Бакалея(Чай/кофе/печенье)', blank=True)
    house_chemicals = models.TextField('Бытовая химия', blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Было потрачено')

    def __str__(self):
        return f" {self.date, self.chancery}"

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'
        ordering = ['-date']


class ContactAdmin(models.Model):
    CHOICES = (
        ('Completed', 'Completed'),
        ('In progress', 'In progress'),
        ('Waiting', 'Waiting'),
    )
    title = models.CharField(max_length=150, verbose_name='Краткое описание')
    description = models.TextField(max_length=512, verbose_name='Описание проблемы')
    response = models.TextField(max_length=512, verbose_name='Ответ администратора', blank=True)
    file = models.FileField(upload_to='file/contact_admin/', verbose_name='Файл', blank=True)
    status = models.CharField(max_length=20, choices=CHOICES, verbose_name="Статус заявки", default='Waiting')
    date = models.DateTimeField(verbose_name='Дата поступления заявки', auto_now_add=True)
    author = models.ForeignKey(AdvUser, verbose_name='Автор заявки', on_delete=models.CASCADE, related_name='author')
    admin = models.ForeignKey(AdvUser, verbose_name='Ответственный за выполнение', on_delete=models.PROTECT, related_name='admin', blank=True, null=True)

    def __str__(self):
        return f"{self.title} | {self.author.first_name} {self.author.last_name}"

    class Meta:
        verbose_name = 'Заявка администратору'
        verbose_name_plural = 'Заявки администратору'
        ordering = ['status', 'date']