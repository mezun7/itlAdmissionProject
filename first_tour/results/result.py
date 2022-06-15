import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
# Create your views here.
# from admission.forms import FileUpload
from admission.models import File, Participant, Moderator, ParticipantRegistrator
from first_tour.models import Tour, ExamResult, NextTourPass, UploadConfirm, ExamSheetScan
from first_tour.results.struct import ResultParticipant
from itlAdmissionProject.settings import SERVER_EMAIL


def get_results():
    tours = Tour.objects.all().order_by('tour_order', 'grade__number', 'profile__name')
    p = UploadConfirm.objects.filter(participant__privilege_status='A')
    print(tours)


def get_result_user(pk, exclude_date=False):
    participant = Participant.objects.get(pk=pk)
    if exclude_date:
        tours = Tour.objects.filter(
            Q(profile=participant.profile) | Q(litergrade__participants__in=[participant]),
            grade=participant.grade,
        ).order_by('tour_order').distinct('tour_order')
    else:
        tours = Tour.objects.filter(
            Q(profile=participant.profile) | Q(litergrade__participants__in=[participant]),
            grade=participant.grade,
            results_release_date__lte=datetime.datetime.now(),
        ).order_by('tour_order').distinct('tour_order')
    results = []
    print(len(tours))
    for tour in tours:
        party_results = ExamResult.objects.filter(
            exam_subject__tour=tour, participant=participant
        ).order_by('exam_subject__ordering')
        print(tour)

        # for pres in party_results:
        #     print(pres.participant, pres.exam_subject.subject, pres.score)
        try:
            passing_type = participant.nexttourpass_set.get(tour=tour)
            # passing_type = NextTourPass.objects.filter(participant=participant).first()
        except NextTourPass.DoesNotExist:
            passing_type = None

        final_release_date = tour.results_release_date
        results.append(
            ResultParticipant(
                party_results,
                result_release_date=final_release_date,
                final_result_release_date=datetime.datetime.now() if exclude_date else tour.final_result_release_date,
                passing_type=passing_type,
                tour=tour,
                portfolio_score=participant.extra_score,
                participant=participant,
            )
        )
    return results
