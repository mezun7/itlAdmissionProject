from admission.forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from admission.models import Participant, Olympiad


def create_user(form: RegisterForm, request, olymp):
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
    participant.out_of_competition = olymp
    participant.came_from_olymp_link = olymp
    participant.save()
    return user, participant
