from openpyxl import Workbook
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from datetime import datetime, date
from action_export.export_excel import ExportExcelAction
from openpyxl.styles import Font
from unidecode import unidecode

from admission.models import Participant
from first_tour.models import Tour, ExamSubject, ExamResult


def get_result(res: ExamResult):
    if res.appeal_score is not None:
        return res.appeal_score
    else:
        res.score


def get_value(obj):
    if obj is None:
        return ''
    return str(obj)


def style_output_file(file):
    black_font = Font(color='000000', bold=True)
    for cell in file["1:1"]:
        cell.font = black_font

    for column_cells in file.columns:
        print([cell.value for cell in column_cells])
        length = max(len(cell.value) for cell in column_cells)
        length += 10
        file.column_dimensions[column_cells[0].column_letter].width = length

    return file


def get_headers(subjects=[]):
    header = [
                 'ID',
                 'ФАМИЛИЯ',
                 'ИМЯ',
                 "ОТЧЕСТВО",
                 'КЛАСС',
                 'Профиль',
             ] + subjects
    return header


def get_correct_str(name: str):
    invalid_chars = ['*', ':', '/', '\\', '?', '[', ']']
    for c in invalid_chars:
        if c in name:
            name = name.replace(c, '')
    return name


def get_sheet_name(tour: Tour):
    return '%s_%s%s' % (get_correct_str(tour.name),
                        get_correct_str(str(tour.grade.number)),
                        '' if tour.profile is None else '_' + get_correct_str(tour.profile.name))


def export_results(self, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied

    tour: Tour = queryset.first()
    wb = Workbook()
    tmp = wb.active
    wb.remove(tmp)

    for tour in queryset.order_by('grade__number'):
        ws = wb.create_sheet(get_sheet_name(tour))
        subjects = ExamSubject.objects.filter(tour=tour).order_by('type_of_scoring')
        header = get_headers([esubj.subject.name for esubj in subjects])
        ws.append(header)
        for participant in Participant.objects.filter(examresult__exam_subject__in=subjects).distinct():
            print(participant)
            info = [str(participant.pk),
                    participant.last_name,
                    participant.first_name,
                    participant.fathers_name,
                    get_value(participant.grade.number),
                    'Нет' if participant.profile is None else participant.profile.name]
            exam_res = []
            for subject in subjects:
                try:
                    eresult = ExamResult.objects.get(participant=participant, exam_subject=subject)
                    exam_res.append(get_result(eresult))
                except:
                    exam_res.append('N/A')
            info = info + exam_res
            ws.append(info)
        # print(info)

    # for participant in queryset.order_by('last_name', 'first_name', 'fathers_name', 'grade'):
    #     if not participant.is_dublicate and participant.first_name is not None:
    #         ws.append([
    #             str(participant.pk),
    #             participant.last_name,
    #             participant.first_name,
    #             participant.fathers_name,
    #             participant.phone_party,
    #             participant.user.email,
    #             get_value(participant.fio_mother),
    #             get_value(participant.phone_mother),
    #             get_value(participant.fio_father),
    #             get_value(participant.phone_father),
    #             get_value(participant.grade.number),
    #             'Нет' if participant.profile is None else participant.profile.name,
    #             participant.school,
    #             str(participant.first_tour_register_date),
    #             get_value(participant.first_tour_come_date)
    #         ])
    # ws = style_output_file(ws)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Participants.xlsx'
    wb.save(response)
    return response


export_results.short_description = 'Export results'
