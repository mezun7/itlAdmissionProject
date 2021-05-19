import datetime

from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth import views as auth_views

from itlAdmissionProject import settings
from itlAdmissionProject.settings import SERVER_EMAIL, REGISTER_END_DATE
from . import views
from first_tour.appeal.teacher_view import appeals_list, appeal_person
from admission import first_tour

urlpatterns = [
    path('main/', views.main, name='test-email'),
    path('appeal/', appeals_list, name='appeal-list'),
    path('appeal/<int:pk>/', appeal_person, name='appeal-person')

]
