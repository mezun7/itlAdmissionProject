import hashlib
import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from admission.forms import RegisterForm, ChildInfo
from admission.models import Participant


def register(request):
    return render(request, 'registration/register.html')


def register_2(request):
    context = {}
    salt = "asdvcx"
    form = RegisterForm()
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            u = User()
            u.username = form.cleaned_data['username']
            u.set_password(form.cleaned_data['password'])
            u.email = form.cleaned_data['email']
            u.is_active = False
            u.save()
            user = u
            # user = authenticate(request, username=u.username, password=form.cleaned_data['password'])
            # print(User)
            login(request, u)
            participant = Participant()
            participant.user = user
            participant.activation_key = hashlib.sha1(salt.encode('utf-8') + str(form.cleaned_data['email']).encode('utf-8')).hexdigest()
            participant.key_expires = datetime.datetime.today() + datetime.timedelta(2)
            participant.save()
            return HttpResponseRedirect(reverse('register3'))
            # TODO
            # Send Email with activation link
    context['form'] = form
    return render(request, 'registration/register2.html', context)


def register_3(request):
    context = {}
    form = ChildInfo()
    context['form'] = form

    return render(request, 'registration/register3.html', context)
