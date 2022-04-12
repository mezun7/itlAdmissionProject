from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail

from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
# from admission.forms import FileUpload
import itlAdmissionProject.settings
from admission.models import File, Participant, Moderator, ParticipantRegistrator, Group, FirstTourDates
from admission.models import Profile
from admission.personal_page.profile import main_page
from first_tour.models import AppealUser
from itlAdmissionProject.settings import SERVER_EMAIL, FILES_COUNT_LIMIT
from .utilities import file_add_extension, file_extension

from django.contrib import messages

from .forms import ChildInfo

import xlwt


def home(request):
    return HttpResponse("Hello!")


def index(request):
    context = {'data': 'index - main page'}
    return render(request, template_name='admission/index.html', context=context)


def proxy_func(request):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(pk=request.user.pk)
            participant = Participant.objects.get(user=request.user)
            if 1 < participant.reg_status < 100:
                return redirect(f'admission:register{participant.reg_status}')
            elif not user.is_active:
                return redirect('admission:register-done')
            elif participant.reg_status == 100:
                return redirect('admission:main')
        except Participant.DoesNotExist:
            try:
                registrator = ParticipantRegistrator.objects.get(user=request.user)
                return redirect('admission:first_tour_register')
            except ParticipantRegistrator.DoesNotExist:
                # Go to the next try clause.
                pass
            try:
                moderator = Moderator.objects.get(user=request.user)
                return redirect('admission:moderator')
            except Moderator.DoesNotExist:
                pass
            try:
                print(request.user)
                au = AppealUser.objects.filter(user=request.user)
                if au is not None and len(au) == 0:
                    raise AppealUser.DoesNotExist
                return redirect('admission:appeal-list')
                # return redirect('first_tour:appeal-list')
            except AppealUser.DoesNotExist:
                print(request.user)
                return redirect('admission:dashboard')
    else:
        return redirect('admission:login')


# @login_required()
# def test_upload(request):
#     if request.method == 'POST':
#         form = FileUpload(request.POST, request.FILES)
#         if form.is_valid():
#             for f in request.FILES.getlist('file'):
#                 file_instance = File(file=f)
#                 file_instance.save()
#     else:
#         form = FileUpload()
#     return render(request, 'registration/base.html', {'form': form})


def test_email(request):
    print(send_mail('Test email', 'test message from django', SERVER_EMAIL, ['sa@litsey7.com', ],
                    fail_silently=False))
    return HttpResponse("Success")


@login_required()
def profile(request):
    participant = Participant.objects.get(user=request.user)
    if participant.reg_status < 100:
        return redirect('admission:proxy')
    return main_page(request)


@login_required()
def profile_change(request):
    participant = Participant.objects.get(user=request.user)
    grade = participant.grade
    edu_profile = participant.profile
    if request.method == 'POST':
        form = ChildInfo(request.POST, instance=participant,  **{'participant': participant})
        # print(form.is_valid())
        if form.is_valid():
            # print(form.is_valid())
            form.save()
            # messages.add_message(request, messages.SUCCESS, 'Объявление исправлено')
            return redirect("admission:main")
    else:
        form = ChildInfo(instance=participant, initial={'user': request.user}, **{'participant': participant})
    context = {
        'form': form,
        'grade': grade,
        'edu_profile': edu_profile,
    }
    return render(request, 'profile/profile_change.html', context)


@login_required()
def diploma_actions(request):
    file_list = Participant.objects.get(user=request.user).portfolio.all()
    file_add_extension(file_list)

    context = {'file_list': file_list, 'files_count_limit': itlAdmissionProject.settings.FILES_COUNT_LIMIT}
    return render(request, 'profile/diploma_actions.html', context)
    pass


@login_required()
def diploma_add(request):
    # file_list = Participant.objects.get(user=request.user).portfolio.all()
    # file_add_extension(file_list)
    files_list = Participant.objects.get(user=request.user).portfolio.all()
    files_count = len(files_list)

    context = {
        'files_count': files_count, 'files_count_limit': FILES_COUNT_LIMIT,
        'reg_status': Participant.objects.get(user=request.user).reg_status
    }
    return render(request, 'profile/diploma_add.html', context)
    pass


@login_required()
def diploma_delete(request, pk):
    participant = Participant.objects.get(user=request.user)
    file = participant.portfolio.get(id=pk)
    file_extension(file)
    if request.method == 'POST':
        file.delete()
        messages.add_message(request, messages.SUCCESS, 'Файл удалён')
        if participant.reg_status == 100:
            return redirect('admission:diploma_actions')
        # elif participant.reg_status == 4:
        #     return redirect('admission:register3')
    else:
        context = {'file': file}
        return render(request, 'profile/diploma_delete.html', context)


@login_required()
def participant_list(request):
    participants = Participant.objects.all().order_by('grade', 'first_name', 'last_name', 'fathers_name')
    paginator = Paginator(participants, 15)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'participants': page.object_list, 'page': page}
    return render(request, 'admission/participant_list.html', context)


def export_participants_xls(request):
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
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    # test = Participant.objects.all()
    rows = Participant.objects.all().values_list(
        'pk', 'first_name', 'last_name', 'fathers_name', 'gender', 'grade',
        'profile', 'lives', 'school',
        'fio_mother', 'phone_mother', 'fio_father', 'phone_father',
    )
    for row in rows:

        # change object pk to value
        row = list(row)
        row[5] = str(Group.objects.get(pk=row[5]))
        if row[6]:
            row[6] = str(Profile.objects.get(pk=row[6]))

        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

