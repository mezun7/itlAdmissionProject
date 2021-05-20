from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.timezone import now

from admission.models import Participant, Profile, Group
from first_tour.result_uploader.rupload import upload

EXAM_TYPES = (
    ('S', 'Балл'),
    ('R', 'Рекомендация'),
    ('Z', 'Зачет')
)

APPEAL_STATUSES = (
    ('N', 'Не заявился'),
    ('Z', 'Заявился'),
)

TYPE_OF_EXAM_PASS = (
    ('R', 'Резерв'),
    ('P', 'Прошел')
)


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Полное имя предмета')
    short_name = models.CharField(max_length=10, verbose_name='Короткое имя предмета')

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name


class Tour(models.Model):
    parent_tour = models.ForeignKey("Tour", blank=True, null=True, on_delete=models.CASCADE, verbose_name='Предыдущий '
                                                                                                          'тур')
    name = models.CharField(max_length=100, verbose_name='Название тура')
    is_final_tour = models.BooleanField(default=False, verbose_name='Финальный тур?')
    results_release_date = models.DateTimeField(verbose_name='Дата опубликования результатов', null=True, blank=True)
    tour_order = models.IntegerField(verbose_name="Какой по счету тур?")
    profile = models.ForeignKey(Profile, verbose_name='Профиль', on_delete=models.CASCADE, null=True, blank=True)
    grade = models.ForeignKey(Group, verbose_name='Класс', on_delete=models.CASCADE, null=True)
    final_result_release_date = models.DateTimeField(verbose_name='Дата опубликования финальных результатов',
                                                     blank=True, null=True)
    appeal_application_end_date = models.DateTimeField(verbose_name='Дата закрытия доступа к аппелляции', blank=True,
                                                       null=True)
    appeal_url = models.CharField(verbose_name='Ссылка на апелляцию', max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

    def __str__(self):
        return '%s (%s: %s)' % (self.name, self.grade, self.profile)


class AppealUser(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Тур')

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи на аппеляцию'


class ExamSubject(models.Model):
    subject = models.ForeignKey(Subject, verbose_name='Предмет', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, verbose_name='Тур', on_delete=models.CASCADE)
    type_of_scoring = models.CharField(max_length=10, verbose_name="Тип оценивания", choices=EXAM_TYPES)
    max_score = models.IntegerField(verbose_name='Максимальный балл')
    passing_score = models.IntegerField(verbose_name='Проходной балл')
    ordering = models.IntegerField(default=100, verbose_name='Позиция в столбце')
    min_score = models.IntegerField(default=0, verbose_name='Минимальный балл')

    class Meta:
        verbose_name = 'Предмет-экзамен'
        verbose_name_plural = "Предметы на экзамены"

    def __str__(self):
        return "%s (%s; %s): %s" % (self.tour.name, self.tour.grade.number, self.tour.profile, self.subject.short_name)


class ExamResult(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, verbose_name='Абитуриент')
    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, verbose_name='Предмет')
    score = models.FloatField(verbose_name='Набранный балл')
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name='Комментарий')
    appeal_application = models.CharField(max_length=10, verbose_name='Заявился на аппеляцию?', blank=True, null=True,
                                          choices=APPEAL_STATUSES)
    appeal_reason = models.CharField(max_length=1000, verbose_name='Причина аппеляции', blank=True, null=True)
    appeal_score = models.IntegerField(verbose_name='Аппелляционный балл', blank=True, null=True)
    is_absent_appeal = models.BooleanField(verbose_name='Отсутствовал на аппелляции', default=False)

    appeal_time = models.DateTimeField(verbose_name='Время аппелляции', blank=True, null=True)
    appeal_user = models.ForeignKey(AppealUser, verbose_name='Учителя аппеллирующий', blank=True, null=True,
                                    on_delete=models.CASCADE)

    def __str__(self):
        return " ".join([str(self.exam_subject), str(self.score)])

    @property
    def get_final_score(self):
        if self.appeal_score is None:
            return self.score
        return self.appeal_score

    class Meta:
        verbose_name = 'Результат экзамена'
        verbose_name_plural = 'Результаты экзаменов'
        unique_together = ('participant', 'exam_subject')


class NextTourPass(models.Model):
    tour = models.ForeignKey(Tour, verbose_name='Тур', on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, verbose_name='Абитуриент', on_delete=models.CASCADE)
    type_of_pass = models.CharField(max_length=2, verbose_name='Прошел?', choices=TYPE_OF_EXAM_PASS)

    def __str__(self):
        return '%s;%s;%s' % (self.participant, self.tour.name, self.type_of_pass)


class UserAppeal(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, verbose_name='Абитуриент')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name=u'Тур')
    is_absent_appeal = models.BooleanField(null=True, blank=True, verbose_name='Пропустил аппелляцию')
    appeal_reason = models.CharField(max_length=2000, verbose_name=u'Причина аппелляции')
    appeal_apply_time = models.DateTimeField(default=now(), verbose_name='Время подачи заявления')


class TourParticipantScan(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, verbose_name='Абитуриент')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Тур')
    scan_file_name = models.CharField(max_length=500, verbose_name="Скан работы")

    def __str__(self):
        return " ".join([self.participant.last_name, self.tour.name, self.scan_file_name])

    class Meta:
        unique_together = ('participant', 'tour')


class TourUploadFile(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name='Тур')
    file = models.FileField(verbose_name='Файл')

    def save(self, *args, **kwargs):
        super(TourUploadFile, self).save(*args, **kwargs)
        upload(self.file.path, self.tour)