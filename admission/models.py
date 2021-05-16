from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from admission.helpers.validators_files import file_size

GENDER_CHOICES = (
    ('M', 'Мужской'),
    ('F', 'Женский'),
)

STATUS_CHOICES = (
    ('N', 'Не проверено'),
    ('R', 'Отклонено'),
    ('A', 'Принято')
)


# Create your models here.
class Moderator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class FirstTourDates(models.Model):
    date = models.DateTimeField(verbose_name='Дата первого тура')

    def __str__(self):
        return 'Придем на 1 тур ' + str(self.date.strftime('%d.%m.%Y')) + ' в ' + str(self.date.strftime('%H:%M'))


class Profile(models.Model):
    name = models.CharField(max_length=100, verbose_name='Профиль обучения')

    def __str__(self):
        return self.name


class Group(models.Model):
    number = models.IntegerField(verbose_name=u'Класс')
    have_profile = models.BooleanField(verbose_name=u'Есть профиль?', default=False)

    def __str__(self):
        return str(self.number)


#
# class Grade(models.Model):
#     number = models.IntegerField(verbose_name='Класс')
#     profile_id = models.ForeignKey(Profile, verbose_name=u'Профиль обучения', on_delete=models.CASCADE, blank=True,
#                                    null=True)
#
#     def __str__(self):
#         return str(self.number)


class FileType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тип файла')


class File(models.Model):
    file_type = models.ForeignKey(FileType, verbose_name='Тип файла', on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(verbose_name='Файл', blank=True, null=True,
                            validators=[FileExtensionValidator(['pdf', 'jpeg', 'jpg', 'png'],
                                                               message='Запрещенный формат файла.'),
                                        file_size
                                        ])

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
    grade = models.ForeignKey(Group, verbose_name='Класс обучения', on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(Profile, verbose_name=u'Профиль обучения', on_delete=models.CASCADE, null=True,
                                blank=True)
    fio_mother = models.CharField(max_length=100, verbose_name='ФИО мамы', null=True, blank=True)
    fio_father = models.CharField(max_length=100, verbose_name='ФИО отца', blank=True, null=True)
    phone_mother = models.CharField(max_length=30, verbose_name='Номер телефона одного из родителей', null=True,
                                    blank=True)
    phone_father = models.CharField(max_length=30, verbose_name='Номер телефона одного из родителей', null=True,
                                    blank=True)
    out_of_competition = models.BooleanField(default=False, verbose_name='Вне конкурса?', null=True, blank=True)
    portfolio = models.ManyToManyField(File, verbose_name='Портфолио', null=True, blank=True)
    reg_status = models.IntegerField(verbose_name='Статус регистрации', default=3)
    activation_key = models.CharField(max_length=500, verbose_name='Ключ активации', null=True, blank=True)
    key_expires = models.DateTimeField(verbose_name='Срок действие ключа истекает', null=True, blank=True)
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    first_tour_register_date = models.ForeignKey(FirstTourDates, verbose_name='Выбранная дата 1 тура',
                                                 blank=True, null=True, on_delete=models.CASCADE)
    phone_party = models.CharField(max_length=30, verbose_name='Номер телефона абитуриента', blank=True, null=True)
    lives = models.CharField(max_length=100, verbose_name='Город проживания', blank=True, null=True)
    portfolio_text = models.CharField(max_length=1000, verbose_name='Список дипломов?', blank=True, null=True)
    privilege_status = models.CharField(max_length=1, verbose_name="Статус проверки льготы", blank=True,
                                        null=True, choices=STATUS_CHOICES)
    date_privilege_check = models.DateTimeField(verbose_name='Дата проверки', blank=True, null=True)
    moderator = models.ForeignKey(Moderator, verbose_name='Кто проверил', blank=True, null=True,
                                  on_delete=models.CASCADE)
    is_dublicate = models.BooleanField(default=False, verbose_name='Дубликат?')
    is_checked = models.BooleanField(default=False, verbose_name='Проверен на дублирование?')
    olymp_coming_status = models.CharField(default='N', verbose_name='Статус прихода', max_length=2)
    first_tour_come_date = models.DateTimeField(blank=True, null=True, verbose_name=u'Пришел')
    extra_score = models.IntegerField(null=True, verbose_name=u'Дополнительные баллы', blank=True)

    # def save(self, *args, **kwargs):
    #     if not self.extra_score:
    #         self.extra_score = None
    #     super(Participant, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Olympiad(models.Model):
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text


class ModeratorMessage(models.Model):
    text = models.CharField(max_length=2000, verbose_name='Сообщение', blank=True, null=True)
    moderator = models.ForeignKey(Moderator, verbose_name=u'Проверено', on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    participant = models.ForeignKey(Participant, verbose_name='Участник', on_delete=models.CASCADE)
    verdict = models.CharField(choices=STATUS_CHOICES, max_length=2, verbose_name='Вердикт')


class ParticipantRegistrator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)
