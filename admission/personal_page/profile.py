import hashlib
import datetime
from django.utils import timezone

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from admission.forms import RegisterForm, ChildInfo
from admission.helpers.appeal_order import get_appeal_order
from admission.helpers.email_ops import get_register_mail
from admission.models import Participant, Olympiad, ModeratorMessage
from first_tour.forms import UserAppealForm
from first_tour.results.result import get_result_user
from itlAdmissionProject.settings import SERVER_EMAIL, APPEAL_PERIOD_MINUTES, APPEAL_START_TIME

from admission.utilities import file_add_extension


@login_required()
def main_page(request):
    participant = Participant.objects.get(user=request.user)
    results = get_result_user(participant.pk)
    a = get_appeal_order(participant)
    appeal_order = APPEAL_START_TIME + datetime.timedelta(minutes=a*APPEAL_PERIOD_MINUTES)
    # print(appeal_order)
    file_list = participant.portfolio.all()
    file_add_extension(file_list)

    context = {
        'participant': participant,
        'messages': ModeratorMessage.objects.filter(participant=participant).order_by('sent_at'),
        'results': results,
        'appeal_order': appeal_order,
        'file_list': file_list,
    }

    if request.POST:
        form = UserAppealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('admission:main'))

    return render(request, 'profile/profile.html', context=context)


@login_required()
def profile_test_page(request):
    participant = Participant.objects.first()
    context = {
        'participant': participant
    }
    return render(request, 'profile/profile.html', context=context)

