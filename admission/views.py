from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
# Create your views here.
# from admission.forms import FileUpload
from admission.models import File, Participant, Moderator
from admission.personal_page.profile import main_page
from itlAdmissionProject.settings import SERVER_EMAIL


def home(request):
    return HttpResponse("Hello!")


def proxy_func(request):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(pk=request.user.pk)
            participant = Participant.objects.get(user=request.user)
            if 1 < participant.reg_status < 100:
                return redirect(f'register{participant.reg_status}')
            elif not user.is_active:
                return redirect('register-done')
            elif participant.reg_status == 100:
                return redirect('main')
        except Participant.DoesNotExist:
            try:
                moderator = Moderator.objects.get(user=request.user)
                return redirect('moderator')
            except Moderator.DoesNotExist:
                return HttpResponse('Something went wrong)')
    else:
        return redirect('login')


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
        return redirect('proxy')
    return main_page(request)
