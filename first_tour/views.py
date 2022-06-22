import psycopg2
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, EmailMessage
# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie

from admission.models import Participant
from .forms import UserAppealForm, TeacherAppealForm
from .forms import UploadForm, ResultUploadForm
from .models import Tour, ExamResult, UploadConfirm, NextTourPass, TourParticipantScan, ExamSheetScan, Subject, \
    ExamSubject
from first_tour.task import test_celery

from django.views.generic.edit import FormView
from .utilities import rename_file
import re
import csv
from io import StringIO


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
    return [
        str(participant.id),
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


# @staff_member_required()
# def test_email(request):
#     email = EmailMessage(email_subject,
#                          email_message,
#                          from_email=SERVER_EMAIL,
#                          to=[request.user.email])
#     email.send()
#     return render(request, 'profile/test.html')
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
    nxt = NextTourPass.objects.filter(tour__tour_order=2).order_by(
        'type_of_pass',
        'tour__grade__number',
        'tour__profile__name',
        'participant__last_name',
        'participant__first_name'
    )
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

@staff_member_required
@ensure_csrf_cookie
def upload_sheets(request):
    tours = Tour.objects.values('tour_order').distinct()
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid() and request.POST['tour_order']:
            tour_order = request.POST['tour_order']
            for f in files:
                file_name_parts = f.name[:f.name.rfind('.')].split('_')
                pk = file_name_parts[0]
                f.name = rename_file(f, f.name)
                ExamSheetScan.objects.create(tour_order=tour_order, participant_id=pk, file=f)
            return redirect('first_tour:exam_sheets')
        context = {'form': form, 'tours': tours}
    else:
        form = UploadForm()
        context = {'form': form, 'tours': tours}
    return render(request, 'first_tour/upload_exam_sheets.html', context=context)


def exam_sheets(request):
    sheets = ExamSheetScan.objects.all().order_by('-tour_order')
    context = {'sheets': sheets}
    return render(request, 'first_tour/exam_sheets.html', context=context)


@staff_member_required
def upload_results(request):
    tour_orders = Tour.objects.values('tour_order').distinct()
    context = None
    if request.method == 'POST':
        form = ResultUploadForm(request.POST, request.FILES)
        if form.is_valid() and request.POST['tour_order']:
            tour_order = request.POST['tour_order']
            csv_file = request.FILES['files']
            results = parse_file(csv_file)
            rows_count = save_results(tour_order, results)
            context = {
                'form': form,
                'msg': f'<div class="alert alert-success">Данные из файла успешно загружены. Тур - {tour_order}. '
                       f'В таблицу БД записано {rows_count} строк</div>',
                'tour_orders': tour_orders,
            }
    else:
        form = ResultUploadForm()
        context = {'form': form, 'tour_orders': tour_orders}
    return render(request, 'first_tour/upload_exam_results.html', context=context)


def parse_file(csv_file):
    file = csv_file.read().decode('utf-8')
    data = []
    reader = csv.DictReader(StringIO(file))
    for row in reader:
        data.append(row)
    return data


def save_results(tour_order, results_from_csv):
    tour = None
    results = []
    subjects = Subject.objects.all().values('id', 'name')
    rows_count = 0
    for s in subjects:
        for r in results_from_csv:
            try:
                if r[s['name']] and r[s['name']] != '#N/A' and r[s['name']] != '':
                    participant = Participant.objects.get(id=r['id'])
                    exam_result = ExamResult()
                    tour = get_tour(tour_order=tour_order, participant=participant)
                    exam_subject = ExamSubject.objects.get(subject__pk=int(s['id']), tour=tour)
                    if tour and exam_subject:
                        rows_count += 1
                        exam_result.participant = participant
                        exam_result.exam_subject = ExamSubject.objects.get(subject__pk=int(s['id']), tour=tour)
                        exam_result.score = float(r[s['name']].replace(',', '.'))
                        results.append(exam_result)
            except Exception as e:
                print('Не могу найти ID участника', r['id'], r, tour, e)
                print(e)
    ExamResult.objects.bulk_create(results)
    return rows_count


def get_tour(tour_order, participant):
    tour = Tour.objects.get(tour_order=tour_order, profile=participant.profile)
    return tour


def load_next_tour_pass(request):
    context = {}
    results = []
    tour_orders = Tour.objects.values('tour_order').distinct()
    if request.method == 'POST':
        tour_order = request.POST['tour_order']
        print(tour_order)
        form = ResultUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['files']
            rows = parse_file(csv_file)
            for row in rows:
                print(row)
                try:
                    participant = Participant.objects.get(id=row['id'])
                    model = NextTourPass()
                    model.participant = participant
                    model.tour = Tour.objects.filter(profile=participant.profile, tour_order=tour_order).first()
                    row['Статус'] = remove_white_spaces(row['Статус'])
                    if row['Статус'] and (row['Статус'].startswith('п') or row['Статус'].startswith('р')):
                        if row['Статус'].startswith('п'):
                            model.type_of_pass = 'P'
                        if row['Статус'].startswith('р'):
                            model.type_of_pass = 'R'
                        results.append(model)
                except Participant.DoesNotExist:
                    print(f"{row['id']} DoesNotExist")
                    participant = None
            try:
                NextTourPass.objects.bulk_create(results)
                msg = f'<div class="alert alert-success">Файл успешно загружен.</div>'
            except Exception or psycopg2.Error as e:
                msg = f'<div class="alert alert-warning">Ошибка: {e}</div>'
            context = {'form': form, 'msg': msg, 'tour_orders': tour_orders}
    else:
        form = ResultUploadForm()
        context = {'form': form, 'tour_orders': tour_orders}
    return render(request, 'first_tour/next_tour_pass.html', context=context)


def remove_white_spaces(string=None):
    if string and len(string) > 0:
        # Remove all non-word characters (everything except numbers and letters)
        return re.sub(r"[^\w\s]", '', string).lower()
    return string

