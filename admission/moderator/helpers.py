from admission.models import Participant


def set_duplicate_status(pk):
    participant = Participant.objects.get(pk=pk)
    participant.is_dublicate = True
    participant.save()


def set_skip_status(pk):
    participant = Participant.objects.get(pk=pk)
    participant.is_checked = True
    participant.save()

