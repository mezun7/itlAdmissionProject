from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from admission.models import Participant, Moderator
from first_tour.models import NextTourPass
from second_tour.models import LiterGradeTutor
from . models import LiterGrade
from django.db.models import F

from psycopg2 import Error


@login_required
@staff_member_required
def check_list(request, pk=None):
    context = {}
    if request.POST:
        has_come = False
        participant_id = request.POST['participant_pk']
        if request.POST.get('has_come', False) == 'on':
            has_come = True
        NextTourPass.objects.filter(participant_id=participant_id).update(has_come=has_come)

    try:
        litergardetutor = LiterGradeTutor.objects.get(participantregistrator__user=request.user)
        litergarde = LiterGrade.objects.get(pk=litergardetutor.litergrade_id)
        participants_list = litergarde.participants.values(
            'last_name', 'first_name', 'fathers_name',
            'grade', 'grade_id', 'pk',
            has_come=F('nexttourpass__has_come')
        )
        context = {'participants_list': participants_list, 'litergarde': litergarde}
    except LiterGradeTutor.DoesNotExist:
        try:
            Moderator.objects.get(user=request.user)
            litergrades = LiterGrade.objects.all()
            if pk:
                litergarde = LiterGrade.objects.get(pk=pk)
                participants_list = litergarde.participants.values(
                    'last_name', 'first_name', 'fathers_name',
                    'grade', 'grade_id', 'pk',
                    litergarde=F('litergrade__name'),
                    has_come=F('nexttourpass__has_come')
                )
                context = {'participants_list': participants_list, 'litergrades': litergrades, 'moderator': True}
                return render(request, template_name='second_tour/check_list.html', context=context)
            else:
                participants_list = LiterGrade.objects.values(
                    last_name=F('participants__last_name'),
                    first_name=F('participants__first_name'),
                    fathers_name=F('participants__fathers_name'),
                    litergarde=F('participants__litergrade__name'),
                    grade=F('participants__grade'),
                    grade_id=F('participants__grade_id'),
                    pk=F('participants__pk'),
                    has_come=F('participants__nexttourpass__has_come')
                )
                context = {'participants_list': participants_list, 'litergrades': litergrades, 'moderator': True}
        except Moderator.DoesNotExist:
            context = {}
    return render(request, template_name='second_tour/check_list.html', context=context)


def get_litergrade_list(request, pk=None):
    litergarde = LiterGrade.objects.get(pk=pk)
    data = litergarde.participants.values(
        'last_name', 'first_name', 'fathers_name',
        'grade', 'grade_id', 'pk',
        litergarde=F('litergrade__name'),
        has_come=F('nexttourpass__has_come')
    )
    return JsonResponse({
        'data': list(data),
        'table_head': ['№', 'Фамилия', 'Имя', 'Отчество', 'Группа', 'Явка на II тур']
    })


def set_has_come(request):
    if request.method == "POST":
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        try:
            NextTourPass.objects.filter(participant_id=post_data['participant_pk']).update(has_come=post_data['has_come'])
            return HttpResponse(0)
        except (Error, Exception) as e:
            return HttpResponse(e)
