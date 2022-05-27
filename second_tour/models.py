from django.db import models
from django.db.models import UniqueConstraint

from first_tour.models import LiterGrade
from admission.models import ParticipantRegistrator


class LiterGradeTutor(models.Model):
    litergrade = models.ForeignKey(LiterGrade, on_delete=models.CASCADE, verbose_name='группа')
    participantregistrator = models.ForeignKey(ParticipantRegistrator, on_delete=models.CASCADE, verbose_name='регистратор')
    UniqueConstraint(fields=['liter_grade', 'participant_registrator'], name='unique_grade_registrator')

    class Meta:
        verbose_name = 'группу II тура'
        verbose_name_plural = 'группы II тура'



