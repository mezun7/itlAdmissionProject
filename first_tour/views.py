from django.contrib.admin.views.decorators import staff_member_required
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie

from admission.models import Participant
from .forms import UserAppealForm, TeacherAppealForm
from .forms import UploadForm, ResultUploadForm
from .models import Tour, ExamResult, UploadConfirm, NextTourPass, TourParticipantScan, ExamSheetScan, Subject
from first_tour.task import test_celery

from django.views.generic.edit import FormView
from .utilities import rename_file
import re


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
    # tour_orders = Tour.objects.values('tour_order', 'name').distinct()
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        # tour_order = request.POST['tour_order']
        files = request.FILES.getlist('files')
        if form.is_valid():
            for f in files:
                file_name_parts = f.name[:f.name.rfind('.')].split('_')
                # print(file_name_parts)
                tour_order = file_name_parts[0]
                pk = file_name_parts[1]
                f.name = rename_file(f, f.name)
                ExamSheetScan.objects.create(tour_order=tour_order, participant_id=pk, file=f)
            # sheets = ExamSheetScan.objects.all()
            # context = {'msg': '<div class="alert alert-success">Файлы успешно загружены</div>', 'sheets': sheets}
            # return render(request, "first_tour/upload_exam_sheets.html", context)
            return redirect('first_tour:exam_sheets')
    else:
        form = UploadForm()
    return render(request, 'first_tour/upload_exam_sheets.html', {'form': form})  # , 'tour_orders': tour_orders})


def exam_sheets(request):
    sheets = ExamSheetScan.objects.all()
    context = {'sheets': sheets}
    return render(request, 'first_tour/exam_sheets.html', context=context)


@staff_member_required
def upload_results(request):

    context = None
    if request.method == 'POST':
        form = ResultUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['files']
            for r in request:
                print(r)
            tour_order = re.findall(r'\d+', str(csv_file))[0]
            results = parse_file(csv_file)
            # for r in results:
            #     print(r)
            # try:
            save_results(tour_order, results)
            # except:
            context = {
                'form': form,
                'msg': f'<div class="alert alert-success">Файл успешно загружен. Тур - {tour_order}</div>'
            }
    else:
        form = ResultUploadForm()
        context = {'form': form}
    return render(request, 'first_tour/upload_exam_results.html', context=context)


import csv
from io import StringIO


def parse_file(csv_file):
    file = csv_file.read().decode('utf-8')
    json_data = []
    # fieldnames = ("participant_id",	"математика", "русский", "биология", "физика")
    fieldnames = set_fieldnames()
    reader = csv.DictReader(StringIO(file), fieldnames)
    for row in reader:
        json_data.append(row)
    json_data.pop(0)
    return json_data


def set_fieldnames():
    subjects = Subject.objects.all().values('id', 'name')
    fieldnames = ['full_name', 'sheet_no', 'exam_date', 'id']
    for s in subjects:
        # fieldnames.append(f'{s["id"]}_{s["name"]}')
        fieldnames.append(s["name"])
    print(fieldnames)
    return tuple(fieldnames)


def save_results(tour_order, results_from_csv):
    # tour = Tour.objects.get(tour_order=tour_order)
    # tour_subjects = tour.examsubject_set.all()
    # for t_subj in tour_subjects:
    #     print(t_subj.subject.name)
    results = []

    subjects = Subject.objects.all().values('id', 'name')
    for s in subjects:
        for r in results_from_csv:
            try:
                participant = Participant.objects.get(id=r['id'])

                # exam_result.participant_id = int(r['id'])
                if r[s['name']] and r[s['name']] != '#N/A' and r[s['name']] != '':
                    exam_result = ExamResult()
                    exam_result.participant = participant
                    exam_result.exam_subject_id = int(s['id'])
                    exam_result.score = float(r[s['name']].replace(',', '.'))
                    results.append(exam_result)
            except Exception as e:
                print('Нет id участника или ', e)

    for r in results:
        print(r.participant.id, r.exam_subject.id)
    ExamResult.objects.bulk_create(results)
