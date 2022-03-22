import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
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
def register_coming(request, grade_id=Group.objects.first().pk):
# def register_coming(request, grade_id=Group.objects.first()):
    context = {
        'participants': Participant.objects.filter(grade_id=grade_id, first_name__isnull=False,
                                                   is_dublicate=False, first_tour_come_date__isnull=True).order_by(
            'last_name', 'first_name', 'fathers_name'),

        'grades': Group.objects.all(),
        'current_grade': Group.objects.get(pk=grade_id),
        'action': reverse('admission:first_tour_register',
                          kwargs={
                              'grade_id': grade_id
                          }),
        'processed': Participant.objects.filter(first_tour_come_date__isnull=False, grade_id=grade_id).count(),
        'overall': Participant.objects.filter(is_dublicate=False, first_name__isnull=False, grade_id=grade_id).count()
    }
    # frst: FirstTourDates = FirstTourDates.objects.first()
    # frst.date.date()
    # Participant.objects.filter(first_tour_register_date__date=)
    action_list = {
        'Дубликат': set_duplicate_status,
        'Пропустить': set_skip_status,
        'Пришел': set_first_tour_coming_status
    }
    if request.POST:
        key = list(request.POST.keys())[-1]
        action_list[request.POST[key]](key)

        return redirect(context['action'])

    return render(request, 'first_tour/register.html', context=context)
