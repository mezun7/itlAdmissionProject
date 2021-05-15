from admission.models import Participant
import datetime


def set_duplicate_status(pk):
    participant = Participant.objects.get(pk=pk)
    participant.is_dublicate = True
    participant.save()


def set_skip_status(pk):
    participant = Participant.objects.get(pk=pk)
    participant.is_checked = True
    participant.save()


def set_olymp_coming_status(pk, status):
    participant = Participant.objects.get(pk=pk)
    participant.olymp_coming_status = status
    participant.save()


def set_refuse_status(pk):
    participant = Participant.objects.get(pk=pk)


def set_first_tour_coming_status(pk):
    participant = Participant.objects.get(pk=pk)
    participant.first_tour_come_date = datetime.datetime.now()
    participant.save()
