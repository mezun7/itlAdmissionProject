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
from first_tour.final_results.final_struct import FinalResult
from first_tour.forms import MarkEditForm
from first_tour.models import Tour, LiterGrade, ExamSubject, ExamResult
from itlAdmissionProject.settings import SERVER_EMAIL
from django.core.mail import send_mail, EmailMessage

SUBJECTS_ORDERING = ('ordering', 'type_of_scoring', 'subject__name')


def get_participants(tour:Tour):
    participants = None
    if tour.all_students_in_rating:
        participants = Participant.objects.filter(profile=tour.profile)
    else:
        for lg in LiterGrade.objects.filter(tour=tour):
            participants = lg.participants.all()
    return participants

@staff_member_required
def main_table(request, tour_ordering=None, tour_id=None):
    tour = None
    if tour_ordering is None:
        tour_ordering = 1
    if tour_id is None:
        try:
            tour = Tour.objects.filter(tour_order=tour_ordering).first()
            print(tour)
        except:
            return HttpResponse('No active tours')
    else:
        tour = Tour.objects.get(pk=tour_id)
    tours = Tour.objects.filter(tour_order=tour_ordering).order_by('grade__number', 'profile')
    exam_subj = ExamSubject.objects.filter(tour=tour).order_by(*SUBJECTS_ORDERING)
    results = []
    participants = get_participants(tour)
    for participant in participants:
        lg = None
        try:
            lg = participant.litergrade_set.get()
        except LiterGrade.DoesNotExist:
            lg = None

        results.append(FinalResult(participant=participant, tour=tour, exam_subjects=exam_subj, liter_grade=lg))
    results.sort(reverse=True)
    context = {
        'tours': tours,
        'subjects': exam_subj,
        'results': results,
        'cur_tour': tour
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
    context = {
        'liters': liters,
        'liter': liter,
        'participants': participants
    }

    return render(request, 'final_results/journal.html', context)


@staff_member_required
def edit_mark(request, mark_id):
    mark = ExamResult.objects.get(pk=mark_id)
    form = MarkEditForm(instance=mark)
    if request.POST:
        form = MarkEditForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            from_url = request.GET.get('from')
            return redirect(from_url)

    context = {
        'form': form,
        'mark': mark
    }
    return render(request, 'final_results/edit_mark.html', context)