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

@login_required()
def moderator(request):
    pass