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
    if request.POST:
        has_come = False
        participant_id = request.POST['participant_pk']
        if request.POST.get('has_come', False) == 'on':
            has_come = True
        NextTourPass.objects.filter(participant_id=participant_id).update(has_come=has_come)

    try:
        Moderator.objects.get(user=request.user)
        litergrades = LiterGrade.objects.values('pk', 'name', grade=F('tour__grade__number'))
        if pk:
            litergarde = LiterGrade.objects.get(pk=pk)
            participants_list = litergarde.participants.values(
                'last_name', 'first_name', 'fathers_name',
                'grade_id', 'pk',
                grade_num=F('grade__number'),
                litergarde=F('litergrade__name'),
                has_come_to=F('nexttourpass__has_come')
            )
            context = {
                'participants_list': sorted(
                    participants_list,
                    key=lambda d: (
                        d['grade_num'],
                        d['last_name'],
                        d['first_name'],
                        d['fathers_name'],
                    )
                ),
                'litergrades': litergrades,
                'moderator': True
            }
            return render(request, template_name='second_tour/check_list.html', context=context)
        else:
            participants_list = NextTourPass.objects.values(
                last_name=F('participant__last_name'),
                first_name=F('participant__first_name'),
                fathers_name=F('participant__fathers_name'),
                litergarde=F('participant__litergrade__name'),
                litergarde_id=F('participant__litergrade__pk'),
                grade_num=F('participant__grade__number'),
                grade_id=F('participant__grade_id'),
                pk=F('participant__pk'),
                has_come_to=F('has_come')
            )

            first_letter = list()
            for l in participants_list:
                fl = str(l['last_name'])[0]
                if fl not in first_letter:
                    first_letter.append(fl)
            first_letter = sorted(first_letter)
            context = {
                'participants_list': sorted(
                    participants_list,
                    key=lambda d: (
                        d['grade_num'],
                        d['last_name'],
                        d['first_name'],
                        d['fathers_name'],
                    )
                ),
                'litergrades': litergrades,
                'first_letter': first_letter,
                'moderator': True
            }
    except Moderator.DoesNotExist:
        try:
            tutor_id = LiterGradeTutor.objects \
                .filter(participantregistrator__user=request.user) \
                .values('participantregistrator_id')[0]['participantregistrator_id']
            litergrades = LiterGrade.objects.filter(litergradetutor__participantregistrator=tutor_id)
            litergrades = litergrades.values('pk', 'name', grade=F('tour__grade__number'))
            if pk:
                litergarde = LiterGrade.objects.get(pk=pk)
                participants_list = litergarde.participants.values(
                    'last_name', 'first_name', 'fathers_name',
                    'grade_id', 'pk',
                    grade_num=F('grade__number'),
                    litergarde=F('litergrade__name'),
                    has_come_to=F('nexttourpass__has_come')
                )
                context = {
                    'participants_list': sorted(
                        participants_list,
                        key=lambda d: (
                            d['grade_num'],
                            d['last_name'],
                            d['first_name'],
                            d['fathers_name'],
                        )
                    ),
                    'litergrades': litergrades,
                    'moderator': True
                }
                return render(request, template_name='second_tour/check_list.html', context=context)
            else:
                # tutor_id = LiterGradeTutor.objects \
                #     .filter(participantregistrator__user=request.user) \
                #     .values('participantregistrator_id')[0]['participantregistrator_id']
                litergrades = LiterGrade.objects.filter(litergradetutor__participantregistrator=tutor_id)
                participants_list = NextTourPass.objects.filter(participant__litergrade__in=litergrades).values(
                    last_name=F('participant__last_name'),
                    first_name=F('participant__first_name'),
                    fathers_name=F('participant__fathers_name'),
                    litergarde=F('participant__litergrade__name'),
                    litergarde_id=F('participant__litergrade__pk'),
                    grade_num=F('participant__grade__number'),
                    grade_id=F('participant__grade_id'),
                    pk=F('participant__pk'),
                    has_come_to=F('has_come')
                )
                litergrades = litergrades.values('pk', 'name', grade=F('tour__grade__number'))
                context = {'participants_list': participants_list, 'litergrades': litergrades}
        except LiterGradeTutor.DoesNotExist:
            context = {}
    return render(request, template_name='second_tour/check_list.html', context=context)


# def get_litergrade_list(request, pk=None):
#     litergarde = LiterGrade.objects.get(pk=pk)
#     data = litergarde.participants.values(
#         'last_name', 'first_name', 'fathers_name',
#         'grade', 'grade_id', 'pk',
#         litergarde=F('litergrade__name'),
#         has_come=F('nexttourpass__has_come')
#     )
#     return JsonResponse({
#         'data': list(data),
#         'table_head': ['№', 'Фамилия', 'Имя', 'Отчество', 'Группа', 'Явка на II тур']
#     })


def set_has_come(request):
    if request.method == "POST":
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        try:
            NextTourPass.objects.filter(participant_id=post_data['participant_pk']).update(has_come=post_data['has_come'])
            return HttpResponse(0)
        except (Error, Exception) as e:
            return HttpResponse(e)


def set_participant_litergrade(request):
    if request.method == "POST":
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        try:
            sql = '''UPDATE first_tour_litergrade_participants
            SET litergrade_id = %s WHERE participant_id=%s'''
            if post_data['old_litergrade']:
                from django.db import connection
                cursor = connection.cursor()
                cursor.execute(sql, [post_data['litergrade_pk'], post_data['participant_pk']])
                connection.commit()
            else:
                lg = LiterGrade.objects.get(pk=post_data['litergrade_pk']);
                lg.participants.add(post_data['participant_pk'])
            return HttpResponse(0)
        except (Error, Exception) as e:
            print(e)
            return HttpResponse(e)


def add_participant(request):
    import json
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        try:
            NextTourPass.objects.filter(participant_id=post_data['participant_pk']).update(
                has_come=post_data['has_come'])
            return HttpResponse(0)
        except (Error, Exception) as e:
            return HttpResponse(e)
    litergrades = LiterGrade.objects.values('pk', 'name', grade=F('tour__grade__number'))
    data = list()
    for item in litergrades:
        data.append(item)
    return HttpResponse(json.dumps(data))
