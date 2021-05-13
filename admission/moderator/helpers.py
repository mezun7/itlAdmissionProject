from admission.models import Participant


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