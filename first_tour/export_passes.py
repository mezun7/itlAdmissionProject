from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from first_tour.action import get_value, get_result
from openpyxl import Workbook


def get_nexttour_passes_headers():
    headers = ["ID", "Тур", "ФИО ребенка", "Класс", "Профиль", "ФИО мамы", "Номер телефона мамы", "ФИО отца",
               "Номер телефона отца"]
    return headers


def export_passes(self, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied

    wb = Workbook()
    tmp = wb.active
    wb.remove(tmp)
    ws = wb.create_sheet('Список')
    header = get_nexttour_passes_headers()
    ws.append(header)
    for result in queryset.order_by("participant__grade__number", "participant__profile",
                                    "participant__last_name", "participant__first_name"):
        info = [
            get_value(result.participant.pk),
            get_value(result.tour.name),
            get_value(' '.join(
                [result.participant.last_name, result.participant.first_name, result.participant.fathers_name])),
            get_value(result.participant.grade.number),
            get_value(result.participant.profile),
            get_value(result.participant.fio_mother),
            get_value(result.participant.phone_mother),
            get_value(result.participant.fio_father),
            get_value(result.participant.phone_father),
        ]
        ws.append(info)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=NextTourPasses.xlsx'
    wb.save(response)
    return response
