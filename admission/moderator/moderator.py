from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
# Create your views here.
# from admission.forms import FileUpload
from django.urls import reverse
from django.views.generic import ListView

from admission.forms import ModeratorMessage2
from admission.models import File, Participant, Moderator, ModeratorMessage
from admission.moderator.helpers import set_duplicate_status, set_skip_status
from admission.moderator.moderator_email import get_moderator_mail
from admission.personal_page.profile import main_page
from itlAdmissionProject.settings import SERVER_EMAIL
from django.core.mail import send_mail, EmailMessage

button_type = {
    'Отклонить': 'R',
    'Подтвердить': 'A',
    'Дубликат': 'D'
}


@staff_member_required
def moderator(request):
    context = {}
    participants = Participant.objects.filter(out_of_competition=True, privilege_status=None,
                                              is_dublicate=False).order_by('grade__number',
                                                                           'first_name',
                                                                           'last_name')
    context['participants'] = participants

    return render(request, 'moderator/index.html', context)


@staff_member_required
def moderate(request, profile_id):
    context = {'form': ModeratorMessage2()}
    moder_user = Moderator.objects.get(user=request.user)
    participant = Participant.objects.get(pk=profile_id)
    if request.POST:
        form = ModeratorMessage2(request.POST)
        if form.is_valid():
            if button_type[request.POST['status']] == 'D':
                participant.is_dublicate = True
                participant.save()
                return redirect('moderator')
            message = form.save(commit=False)
            message.moderator = moder_user
            message.participant = participant
            message.verdict = button_type[request.POST['status']]
            participant.privilege_status = message.verdict
            message.save()
            participant.save()
            email_subject, email_message = get_moderator_mail(message.verdict, message.text,
                                                              participant.first_tour_register_date)
            email = EmailMessage(email_subject,
                                 email_message,
                                 from_email=SERVER_EMAIL,
                                 to=[participant.user.email])
            email.send()
            return redirect('moderator')

        # print()

    try:

        context['participant'] = participant
        context['portfolio'] = participant.portfolio.all()

        return render(request, 'moderator/moderate_profile.html', context)
    except Participant.DoesNotExist:
        return render(request, 'moderator/moderate_profile.html')


@staff_member_required
def dublicate_check(request):
    participants = Participant.objects.filter(Q(out_of_competition=False) | Q(out_of_competition__isnull=True),
                                              is_dublicate=False,
                                              first_name__isnull=False,
                                              is_checked=False).order_by('last_name',
                                                                         'first_name')
    context = {
        'participants': participants,
        'accept': 'Дубликат',
        'reject': 'Пропустить',
        'action': reverse('dublicate')
    }
    action_list = {
        'Дубликат': set_duplicate_status,
        'Пропустить': set_skip_status
    }
    if request.POST:
        key = list(request.POST.keys())[-1]
        action_list[request.POST[key]](key)
        return redirect('dublicate')

    return render(request, 'moderator/dublicate_check.html', context)



