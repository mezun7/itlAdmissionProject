import hashlib
import datetime

from django.contrib.admin.views.decorators import staff_member_required
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
from admission.models import Participant, Olympiad


@staff_member_required
def dashboard_main(request):
    participant = Participant.objects.first()
    context = {
        'participant': participant
    }

    return render(request, 'dashboard/main-dashboard.html', context=context)
