from django.contrib.admin.views.decorators import staff_member_required
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from admission.models import Participant
from first_tour.forms import UserAppealForm, TeacherAppealForm
from first_tour.models import Tour, ExamResult, UploadConfirm, NextTourPass
from first_tour.task import test_celery


def get_party_register(participant: Participant):
    try:
        UploadConfirm.objects.get(participant=participant)
        return 'True'
    except:
        return 'False'


def get_part_info(participant: Participant):
    return [str(participant.id),
            ' '.join([participant.last_name, participant.first_name, participant.fathers_name]),
            str(participant.grade.number),
            participant.profile.name,
            participant.school,
            get_party_register(participant)
            ]


def main(request):
    # test_celery.delay(1)
    tour = Tour.objects.first()
    participant = Participant.objects.first()
    formSetQuery = ExamResult.objects.filter(participant_id=4)
    FormSet = modelformset_factory(model=ExamResult, form=TeacherAppealForm, max_num=len(formSetQuery))
    formset = FormSet(queryset=formSetQuery)
    if request.POST:
        formset2 = FormSet(request.POST)
        print(formset.errors)
        if formset2.is_valid():
            formset2.save()
            print('Here')

    print(tour.id)
    context = {
        'formset': formset
    }
    # if request.POST:
    #     formset = FormSet(request.POST, queryset=formSetQuery)
    #     if formset.is_valid():
    #         formset.save()
    return render(request, 'profile/test.html', context=context)


@staff_member_required
def get_registered(request):
    nxt = NextTourPass.objects.all()
    s = 'id;fio;grade;profile;school;registration\n'
    for u in nxt:
        tmp = ';'.join(get_part_info(u.participant))
        s = s + tmp + '\n'
    # print(s)
    return HttpResponse(s, content_type="text/plain; charset=utf-8")
