from django.contrib.auth.models import User
from django.db import models

GENDER_CHOICES = (
    ('M', 'Мужской'),
    ('F', 'Женский'),
)


# Create your models here.

class FirstTourDates(models.Model):
    date = models.DateTimeField(verbose_name='Дата первого тура')

    def __str__(self):
        return str(self.date)


class Profile(models.Model):
    name = models.CharField(max_length=100, verbose_name='Профиль обучения')

    def __str__(self):
        return self.name


class Grade(models.Model):
    number = models.IntegerField(verbose_name='Класс')
    profile_id = models.ForeignKey(Profile, verbose_name=u'Профиль обучения', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)


class FileType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тип файла')


class File(models.Model):
    file_type = models.ForeignKey(FileType, verbose_name='Тип файла', on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to='files/', verbose_name='Файл', blank=True, null=True)

    def __str__(self):
        return str(self.file)


class Participant(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователь', null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=200, verbose_name='Фамилия', null=True, blank=True)
    fathers_name = models.CharField(max_length=100, verbose_name='Отчество', null=True, blank=True)
    birthday = models.DateField(verbose_name='Дата рождения абитуриента', null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, verbose_name='Место рождения абитуриента', null=True, blank=True)
    school = models.CharField(max_length=100, verbose_name='Школа', null=True, blank=True)
    grade = models.ForeignKey(Grade, verbose_name='Класс обучения', on_delete=models.CASCADE, null=True, blank=True)
    fio_mother = models.CharField(max_length=100, verbose_name='ФИО мамы', null=True, blank=True)
    fio_father = models.CharField(max_length=100, verbose_name='ФИО отца', blank=True, null=True)
    phone_mother = models.CharField(max_length=30, verbose_name='Номер телефона одного из родителей', null=True,
                                    blank=True)
    phone_father = models.CharField(max_length=30, verbose_name='Номер телефона одного из родителей', null=True,
                                    blank=True)
    out_of_competition = models.BooleanField(default=False, verbose_name='Вне конкурса?', null=True, blank=True)
    portfolio = models.ManyToManyField(File, verbose_name='Портфолио', null=True, blank=True)
    reg_status = models.IntegerField(verbose_name='Статус регистрации', default=3)
    activation_key = models.CharField(max_length=500, verbose_name='Ключ активации')
    key_expires = models.DateTimeField(verbose_name='Срок действие ключа истекает')
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    first_tour_register_date = models.ForeignKey(FirstTourDates, verbose_name='Выбранная дата 1 тура',
                                                 blank=True, null=True, on_delete=models.CASCADE)
    phone_party = models.CharField(max_length=30, verbose_name='Номер телефона абитуриента', blank=True, null=True)
    lives = models.CharField(max_length=100, verbose_name='Город проживания', blank=True, null=True)
    portfolio_text = models.CharField(max_length=1000, verbose_name='Список дипломов?', blank=True, null=True)

    def __str__(self):
        return self.user.username

