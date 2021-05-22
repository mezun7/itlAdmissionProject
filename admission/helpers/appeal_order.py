from first_tour.models import UserAppeal


def get_appeal_order(participant):
    uas = UserAppeal.objects.all().order_by('id')
    for ind, ua in enumerate(uas):
        if ua.participant == participant:
            return ind
    return 100000
