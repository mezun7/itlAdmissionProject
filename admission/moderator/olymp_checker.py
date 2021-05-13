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
from admission.models import File, Participant, Moderator, ModeratorMessage
from admission.moderator.helpers import set_duplicate_status, set_skip_status, set_olymp_coming_status
from admission.moderator.moderator_email import get_moderator_mail
from admission.personal_page.profile import main_page
from itlAdmissionProject.settings import SERVER_EMAIL
from django.core.mail import send_mail, EmailMessage


@staff_member_required
def olymp_list(request):
    participants = Participant.objects.filter(privilege_status__iexact='A', olymp_coming_status='N')
    context = {
        'participants': participants,
        'accept': 'Придет',
        'reject': 'Отказ',
        'action': reverse('checker'),
    }

    action_list = {
        'Отказ': 'R',
        'Придет': 'A'
    }

    if request.POST:
        key = list(request.POST.keys())[-1]
        set_olymp_coming_status(key, action_list[request.POST[key]])
        return redirect('checker')
    return render(request, 'moderator/olymp_coming_check.html', context)
