from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from admission.models import Participant
from first_tour.forms import UserAppealForm, TeacherAppealForm
from first_tour.models import Tour, ExamResult
from first_tour.task import test_celery


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
