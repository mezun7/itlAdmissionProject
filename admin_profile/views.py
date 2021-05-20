from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

import hashlib
import datetime
from django.utils import timezone

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from admin_profile.helpers.user_struct import ListStruct
from admission.forms import RegisterForm, ChildInfo
from admission.helpers.email_ops import get_register_mail, get_email_with_results
from admission.models import Participant, Olympiad, ModeratorMessage
from first_tour.appeal.teacher_view import AppealStruct
from first_tour.forms import UserAppealForm
from first_tour.models import UserAppeal
from first_tour.results.result import get_result_user
from first_tour.task import make_mailing
from itlAdmissionProject.settings import SERVER_EMAIL


@staff_member_required
def user_page(request, pk):
    # user = request.user  # type: User
    participant = Participant.objects.get(pk=pk)
    results = get_result_user(participant.pk, exclude_date=True)
    context = {
        'participant': participant,
        'messages': ModeratorMessage.objects.filter(participant=participant).order_by('sent_at'),
        'results': results
    }

    if request.POST:
        form = UserAppealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('main'))

    return render(request, 'profile/profile.html', context=context)


@staff_member_required
def profiles_page(request):
    participants = Participant.objects.filter(is_dublicate=False, first_tour_come_date__isnull=False)

    results = []
    context = {
        'results': results,
        'now': datetime.datetime.now()

    }
    for participant in participants:
        results.append(ListStruct(participant))

    return render(request, 'admin_profile/user_list.html', context=context)


@staff_member_required
def send_results(request):
    participants = Participant.objects.filter(is_dublicate=False, first_tour_come_date__isnull=False)
    make_mailing.delay(email_subject='Started', email_message='Started mailing', email='sa@kpfu.ru')
    for participant in participants:
        email_subject, email_message = get_email_with_results(participant)
        make_mailing.delay(email_subject=email_subject, email_message=email_message, email=participant.user.email)
    return HttpResponse('Started')


@staff_member_required
def send_test(request):
    for i in range(10):
        make_mailing.delay(email_subject='Sorry', email_message='Testing email', email='sa@kpfu.ru')
    return HttpResponse('Started')