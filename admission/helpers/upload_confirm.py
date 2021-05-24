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
from admission.helpers.appeal_order import get_appeal_order
from admission.helpers.email_ops import get_register_mail, get_email_with_results
from admission.models import Participant, Olympiad, ModeratorMessage
from first_tour.appeal.teacher_view import AppealStruct
from first_tour.forms import UserAppealForm, UserConfirmForm
from first_tour.models import UserAppeal
from first_tour.results.result import get_result_user
from first_tour.task import make_mailing
from itlAdmissionProject.settings import SERVER_EMAIL, APPEAL_START_TIME, APPEAL_PERIOD_MINUTES


@login_required
def upload_confirm(request, pk):
    if request.POST:
        form = UserConfirmForm(request.POST, request.FILES)
        print(request.FILES, request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return redirect('main')
