from django.db import models

# Create your models here.
from admission.models import Participant


class Error(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Время ошибки')
    participant = models.ForeignKey(Participant, blank=True, null=True, verbose_name='Участник', on_delete=models.CASCADE)
    message = models.CharField(max_length=3000, verbose_name='Ошибка')
    party_id = models.IntegerField(max_length=100, verbose_name='ID текстом', blank=True, null=True)

    def __str__(self):
        return str(self.date) + " " + self.message
