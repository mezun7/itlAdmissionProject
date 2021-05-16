import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
# Create your views here.
# from admission.forms import FileUpload
from django.urls import reverse
from django.views.generic import ListView

from admission.forms import ModeratorMessage2
from admission.models import File, Participant, Moderator, ModeratorMessage, Group, FirstTourDates
from admission.moderator.helpers import set_duplicate_status, set_skip_status, set_olymp_coming_status, \
    set_first_tour_coming_status
from admission.moderator.moderator_email import get_moderator_mail
from admission.personal_page.profile import main_page
from itlAdmissionProject.settings import SERVER_EMAIL
from django.core.mail import send_mail, EmailMessage


@staff_member_required
def set_extra_score(request):
    participants = Participant.objects.filter(Q(privilege_status__iexact='R') | Q(privilege_status__isnull=True),
                                              portfolio__file__isnull=False, extra_score__isnull=True,
                                              is_dublicate=False).distinct().annotate(num_diplomas=Count('portfolio')).order_by('-num_diplomas','last_name', 'first_name')
    paginator = Paginator(participants, 10)
    page_number = int(request.GET.get('page'))
    page_obj = paginator.get_page(page_number)
    if int(page_number) > page_obj.paginator.num_pages:
        page_number = page_obj.paginator.num_pages
    context = {
        'participants': page_obj,
        'left': len(participants),
        'action': "%s?page=%d" % (reverse('set_extra_score'), page_number),
        'accept': '+10',
        'reject': '+5',
        'skip': '0',
        'page_obj': page_obj
    }
    action_list = {
        '+10': 10,
        '+5': 5,
        '0': 0
    }

    if request.POST:
        key = list(request.POST.keys())[-1]
        participant = Participant.objects.get(pk=key)
        participant.extra_score = action_list[request.POST[key]]
        participant.save()
        return redirect(context['action'])

    return render(request, 'moderator/dublicate_check.html', context=context)


class ExtraScoreView(ListView):
    paginate_by = 1
    model = Participant