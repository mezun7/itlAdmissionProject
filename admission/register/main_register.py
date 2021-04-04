import hashlib
import datetime
from django.utils import timezone

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from admission.forms import RegisterForm, ChildInfo
from admission.helpers.email_ops import get_register_mail
from admission.models import Participant, Olympiad
from itlAdmissionProject.settings import SERVER_EMAIL

salt = "asdvcx"


def register(request):
    if request.user.is_authenticated:
        return redirect('proxy')
    return render(request, 'registration/register.html')


def register_2(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('proxy')

    form = RegisterForm()
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            u = User()
            u.username = form.cleaned_data['username']
            u.set_password(form.cleaned_data['password'])
            u.email = form.cleaned_data['email']
            u.is_active = True
            u.save()
            user = u
            # user = authenticate(request, username=u.username, password=form.cleaned_data['password'])
            # print(User)
            login(request, u)
            participant = Participant()
            participant.user = user
            participant.grade = form.cleaned_data['grade_to_enter']
            participant.activation_key = form.cleaned_data['password']
            participant.save()

            return HttpResponseRedirect(reverse('register3'))
            # TODO
            # Send Email with activation link

    context['form'] = form

    return render(request, 'registration/register2.html', context)


@login_required()
def register_3(request):
    context = {}
    form = ChildInfo(instance=Participant.objects.get(user=request.user))
    context['olympiads'] = [olympiad.text for olympiad in Olympiad.objects.all()]
    if request.POST:
        form = ChildInfo(request.POST, instance=Participant.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            participant = Participant.objects.get(user=request.user)
            participant.reg_status = 4
            participant.save()
            return redirect('register4')
        else:
            pass
            # print(form.cleaned_data['birthday'])
    context['form'] = form
    return render(request, 'registration/register3.html', context)


# @login_required()
# def register_4(request):
#     context = {'form': FileUploadForm()}
#     return render(request, 'registration/register4.html', context)


def confirm(request, activation_key):
    context = {}
    try:
        participant = Participant.objects.get(activation_key=activation_key)
        user = participant.user
        user.is_active = True
        user.save()
        context = {
            'type': True,
            'title': "Успех",
            'message': "Вы успешно подтвердили свой email. Мы вас перенаправим на другую страницу."
        }
        return render(request, 'registration/error.html', context)
    except (User.DoesNotExist, Participant.DoesNotExist):
        error = ''
        context = {
            'type': False,
            'title': "Ошибка",
            'message': "Неверный ключ активации."
        }
        return render(request, 'registration/error.html', context)


@login_required()
def register_complete(request):
    participant = Participant.objects.get(user=request.user)
    password = participant.activation_key[:]
    participant.activation_key = hashlib.sha1(
        salt.encode('utf-8') + str(request.user.email).encode('utf-8')).hexdigest()
    participant.key_expires = datetime.datetime.today() + datetime.timedelta(2)
    participant.reg_status = 100
    participant.save()
    print(participant.user.username)
    user = User.objects.get(pk=request.user.pk)
    user.is_active = False
    user.save()

    email_subject, email_message = get_register_mail(username=participant.user.username,
                                                     activation_key=participant.activation_key
                                                     )
    email = EmailMessage(email_subject,
                         email_message,
                         from_email=SERVER_EMAIL,
                         to=[request.user.email])
    email.send()
    return render(request, 'registration/register_done.html')


def activate_email(request):
    return render(request, 'registration/register_done.html')
