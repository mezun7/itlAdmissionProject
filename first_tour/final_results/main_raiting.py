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
from first_tour.models import Tour, LiterGrade
from itlAdmissionProject.settings import SERVER_EMAIL
from django.core.mail import send_mail, EmailMessage


@staff_member_required
def main_table(request, tour_id=None):
    if tour_id is None:
        tour_id = Tour.objects.first().pk
    tour = Tour.objects.get(pk=tour_id)
    tours = Tour.objects.filter().order_by('grade__number')
    context = {
        'tours': tours
    }

    return render(request, 'final_results/main-table.html', context=context)


@staff_member_required
def journal_with_photos(request, liter_id=None):
    liters = LiterGrade.objects.all().order_by('tour__grade__number', 'name')
    liter = liters.first()
    if liter_id is not None:
        try:
            liter = LiterGrade.objects.get(pk=liter_id)
        except LiterGrade.DoesNotExist:
            print(liter_id, 'Does\'nt exists')
    participants = liter.participants.all().order_by('last_name', 'first_name')
    print(liter)
    context = {
        'liters': liters,
        'liter': liter,
        'participants': participants
    }

    return render(request, 'final_results/journal.html', context)
