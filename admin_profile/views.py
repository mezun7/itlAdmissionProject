from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

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
from admission.helpers.email_ops import get_register_mail
from admission.models import Participant, Olympiad, ModeratorMessage
from first_tour.appeal.teacher_view import AppealStruct
from first_tour.forms import UserAppealForm
from first_tour.models import UserAppeal
from first_tour.results.result import get_result_user
from itlAdmissionProject.settings import SERVER_EMAIL


@staff_member_required
def user_page(request, pk):
    # user = request.user  # type: User
    participant = Participant.objects.get(pk=pk)
    results = get_result_user(participant.pk)
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
    userAppeals = UserAppeal.objects.filter().order_by('appeal_apply_time')
    results = []
    context = {
        'results': results,
        'admin': True
    }

    for ua in userAppeals:
        participant = ua.participant
        tour = ua.tour
        examResults = participant.examresult_set.filter(exam_subject__in=tour.examsubject_set.all()).order_by(
            'exam_subject__type_of_scoring')
        results.append(AppealStruct(participant=participant,
                                    appeal=ua,
                                    subjects=examResults,
                                    tour=tour
                                    )
                       )
        print(examResults)

    return render(request, 'first_tour/appeal_list.html', context=context)
