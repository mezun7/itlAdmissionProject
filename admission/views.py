from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
# from admission.forms import FileUpload
from admission.models import File, Participant, Moderator, ParticipantRegistrator, Group, FirstTourDates
from admission.personal_page.profile import main_page
from first_tour.models import AppealUser
from itlAdmissionProject.settings import SERVER_EMAIL

from django.contrib import messages

from .forms import ChildInfo


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
        print(form.is_valid())
        if form.is_valid():
            print(form.is_valid())
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
