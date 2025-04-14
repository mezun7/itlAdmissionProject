import logging

import xlwt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from admission.actions import get_value
from admission.models import Participant, Moderator
from first_tour.models import NextTourPass, UploadConfirm
from second_tour.models import LiterGradeTutor
from .models import LiterGrade
from django.db.models import F

from django.contrib.auth.models import User
import cyrtranslit

from psycopg2 import Error


def get_participants_list(litergrade=None):
    participants = NextTourPass.objects.all()
    if litergrade:
        participants = NextTourPass.objects.filter(participant__litergrade=litergrade)

    participants = participants.order_by('participant__grade__number',
                          'participant__profile', 'has_come',
                          'participant__last_name',
                          'participant__first_name')

    return participants


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
        litergrades = LiterGrade.objects.values(
            'pk', 'name', grade=F('tour__grade__number')
        ).order_by('tour__grade__number', 'name')
        if pk:
            litergarde = LiterGrade.objects.get(pk=pk)

            participants_list = get_participants_list(litergarde)

            print(participants_list)
            context = {
                'participants': participants_list,
                'litergrades': litergrades,
                'moderator': True
            }
            return render(request, template_name='second_tour/check_list.html', context=context)
        else:
            participants = get_participants_list()

            first_letter = set()
            for l in participants:
                fl = str(l.participant.last_name)[0]
                first_letter.add(fl)

            first_letter = sorted(first_letter)
            print(first_letter)
            context = {

                'litergrades': litergrades,
                'first_letter': first_letter,
                'moderator': True,
                'participants': participants,
            }
    except Moderator.DoesNotExist:
        try:
            tutor_id = LiterGradeTutor.objects \
                .filter(participantregistrator__user=request.user) \
                .values('participantregistrator_id')[0]['participantregistrator_id']
            litergrades = LiterGrade.objects.filter(litergradetutor__participantregistrator=tutor_id)
            litergrades = litergrades.values(
                'pk', 'name', grade=F('tour__grade__number')
            ).order_by('tour__grade__number', 'name')
            if pk:
                litergarde = LiterGrade.objects.get(pk=pk)
                participants_list = get_participants_list(litergarde)
                context = {
                    'participants': participants_list,
                    'litergrades': litergrades,
                }
                return render(request, template_name='second_tour/check_list.html', context=context)
            else:
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
                    has_come_to=F('has_come'),
                    profile=F('participant__profile__name'),
                    olymp_status=F('participant__privilege_status'),
                    confirmed_participation=F('participant__uploadconfirm__pps')
                )
                litergrades = litergrades.values(
                    'pk', 'name', grade=F('tour__grade__number')
                ).order_by('tour__grade__number', 'name')
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
            NextTourPass.objects.filter(participant_id=post_data['participant_pk']).update(
                has_come=post_data['has_come'])
            return HttpResponse(0)
        except (Error, Exception) as e:
            return HttpResponse(e)


def set_participant_litergrade(request):
    if request.method == "POST":
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        try:
            sql = """UPDATE first_tour_litergrade_participants
            SET litergrade_id = %s WHERE participant_id=%s"""
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


def exclude_participant(request):
    if request.method == "POST":
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        if post_data['exclude']:
            try:
                sql = 'DELETE FROM first_tour_litergrade_participants WHERE participant_id =%s'
                from django.db import connection
                cursor = connection.cursor()
                cursor.execute(sql, (post_data['participant_pk'],))
                connection.commit()
                return HttpResponse(0)
            except (Error, Exception) as e:
                print(e)
                return HttpResponse(e)


def add_participant(request):
    import json
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        try:
            password = User.objects.make_random_password();
            user = User(
                username=None,
                email=post_data['email'],
                is_active=True
            )
            user.set_password(password)
            set_username(user, post_data['name'])
            user.save()
            from admission.models import Group
            grade = Group.objects.get(number=post_data['grade'])
            participant = Participant(
                last_name=post_data['surname'],
                first_name=post_data['name'],
                fathers_name=post_data['patronymic'],
                fio_mother=post_data['parent_name'],
                phone_mother=post_data['phone'],
                reg_status=100,
                is_checked=True,
                gender=post_data['gender'],
                grade=grade,
                user_id=user.pk,
            )
            participant.save()
            data = {'login': user.username, 'password': password}
            return JsonResponse(data)
            # return HttpResponse(data)
        except Error as e:
            print(e.pgcode)
            # data = {'error': e}
            return HttpResponse(e)
    litergrades = LiterGrade.objects.values('pk', 'name', grade=F('tour__grade__number'))
    data = list()
    for item in litergrades:
        data.append(item)
    return HttpResponse(json.dumps(data))


def set_username(user, first_name):
    first_name = cyrtranslit.to_latin(first_name.lower().replace('ь', '').replace('Ъ', ''), 'ru')
    username = None
    if not user.username:
        username = first_name
        counter = 1
        while User.objects.filter(username=username):
            username = first_name + str(counter)
            counter += 1
        user.username = username


@staff_member_required()
def get_participants(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Participants_list.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Участники')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
        'ID', 'Фамилия', 'Имя', 'Отчество', 'Пол', 'Класс',
        'Профиль обучения', 'Город проживания', 'Школа',
        'ФИО матери', 'Телефон матери', 'ФИО отца', 'Телефон отца',
        'Литера', 'Явка на второй тур?'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    # test = Participant.objects.all()
    liters = LiterGrade.objects.all().order_by('tour', 'name')
    logging.info(str(liters))
    print(str(liters))
    for liter in liters:
        participants = liter.participants.all()
        # print(len(participants))
        # change object pk to value
        for participant in participants:
            try:
                came = NextTourPass.objects.get(participant=participant).has_come
            except NextTourPass.DoesNotExist:
                came = False
            tmp = [get_value(elem) for elem in
                   [
                       participant.pk,
                       participant.last_name,
                       participant.first_name,
                       participant.fathers_name,
                       participant.gender,
                       participant.grade.number,
                       participant.profile,
                       participant.lives,
                       participant.school,
                       participant.fio_mother,
                       participant.phone_mother,
                       participant.fio_father,
                       participant.phone_father,
                       liter.name,
                       came
                   ]
                   ]

            row_num += 1
            for col_num in range(len(tmp)):
                ws.write(row_num, col_num, tmp[col_num], font_style)

    wb.save(response)
    return response
