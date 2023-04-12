from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from openpyxl import Workbook

from first_tour.action import get_value, get_result
from first_tour.models import ExamResult, Subject


def get_appeal_header(subjects=[]):
    header = [
                 'ID',
                 'ФИО ученика',
                 'Класс',
                 'Профиль',
                 'ФИО родителя 1',
                 "ФИО родителя 2",
                 "Причина"
             ] + subjects
    return header


def export_appeals_list(self, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied

    wb = Workbook()
    tmp = wb.active
    wb.remove(tmp)
    ws = wb.create_sheet('Список на апелляцию')
    subjects = [subject.name for subject in Subject.objects.all().order_by('pk')]
    header = get_appeal_header(subjects)
    ws.append(header)
    for result in queryset:
        info = [
            get_value(result.participant.pk),
            get_value(' '.join(
                [result.participant.last_name, result.participant.first_name, result.participant.fathers_name])),
            get_value(result.participant.grade.number),
            get_value(result.participant.profile),
            get_value(result.participant.fio_mother),
            get_value(result.participant.fio_father),
            get_value(result.appeal_reason),
        ]
        exam_res = []
        for subject in subjects:
            try:
                eresult = ExamResult.objects.get(participant=result.participant, exam_subject=subject)
                exam_res.append(get_result(eresult))
            except:
                exam_res.append('N/A')
        info = info + exam_res
        ws.append(info)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=ExamResults.xlsx'
    wb.save(response)
    return response
