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


def get_value(obj):
    if obj is None:
        return '-'
    return obj.name


def get_value_str(obj):
    if obj is not None:
        return str(obj)
    else:
        return '-'


def get_part_info(participant: Participant):
    return [str(participant.id),
            ' '.join([participant.last_name, participant.first_name, participant.fathers_name]),
            get_value_str(participant.phone_party),
            str(participant.grade.number),
            get_value(participant.profile),
            participant.school,
            get_party_register(participant),
            get_value_str(participant.fio_mother),
            get_value_str(participant.phone_mother),
            get_value_str(participant.fio_father),
            get_value_str(participant.phone_father)
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
    nxt = NextTourPass.objects.filter(tour__tour_order=2).order_by('type_of_pass',
                                                                   'tour__grade__number',
                                                                   'tour__profile__name',
                                                                   'participant__last_name',
                                                                   'participant__first_name')
    s = 'id;fio;phone;grade;profile;school;registration;parent1;phone1;parent2;phone2\n'
    for u in nxt:
        tmp = ';'.join(get_part_info(u.participant) + [u.type_of_pass])
        s = s + tmp + '\n'
    # print(s)
    return HttpResponse(s, content_type="text/plain; charset=utf-8")


# def get_passed(request):
#     nxt = NextTourPass.objects.filter(tour__tour_order=2).order_by('tour__grade__number', 'tour__profile__name')
#     s = 'id;fio;phone;grade;profile;school;registration;parent1;phone1;parent2;phone2\n'
#     for u in