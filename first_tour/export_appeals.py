from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from openpyxl import Workbook

from first_tour.action import get_value, get_result
from first_tour.models import ExamResult, Subject, ExamSubject, ExamSheetScan
from itlAdmissionProject.settings import MAIN_HOST


def get_examsheet_url(tour, participant):
    try:
        scan = ExamSheetScan.objects.filter(
            tour_order=tour.tour_order, participant=participant
        ).order_by('-id')[0]
        main_url = MAIN_HOST[:-1] + scan.file.url
        url = '=HYPERLINK("{}", "{}")'.format(main_url, main_url)
        return url
    except:
        return ''


def get_appeal_header(subjects=[]):
    header = [
                 'ID',
                 'Тур',
                 'ФИО ученика',
                 'Класс',
                 'Профиль',
                 'ФИО родителя 1',
                 "ФИО родителя 2",
                 "Причина",
                 "Ссылка на работу"
             ] + subjects
    return header


def export_appeals_list(self, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied

    wb = Workbook()
    tmp = wb.active
    wb.remove(tmp)
    ws = wb.create_sheet('Список на апелляцию')
    subjects = Subject.objects.all().order_by('pk')
    header = get_appeal_header([subject.name for subject in subjects])
    ws.append(header)
    for result in queryset:
        info = [
            get_value(result.participant.pk),
            get_value(result.tour.name),
            get_value(' '.join(
                [result.participant.last_name, result.participant.first_name, result.participant.fathers_name])),
            get_value(result.participant.grade.number),
            get_value(result.participant.profile),
            get_value(result.participant.fio_mother),
            get_value(result.participant.fio_father),
            get_value(result.appeal_reason),
            get_value(get_examsheet_url(result.tour, result.participant))
        ]
        exam_res = []
        for subject in subjects:
            try:
                esubject = ExamSubject.objects.get(subject=subject, tour=result.tour)
                eresult = ExamResult.objects.get(participant=result.participant, exam_subject=esubject)
                exam_res.append(get_value(eresult.appeal_score))
            except:
                exam_res.append('N/A')
        info = info + exam_res
        ws.append(info)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=AppealsList.xlsx'
    wb.save(response)
    return response
