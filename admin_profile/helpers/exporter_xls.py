import xlwt
from django.http import HttpResponse


def get_xls(data, sheet_name='Информация'):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Participants_list.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(sheet_name)
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for row_num, row in enumerate(data):
        for col_num, col in enumerate(row):
            ws.write(row_num, col_num, col, font_style)
    wb.save(response)
    return response
