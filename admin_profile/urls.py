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
    path('profile/<int:pk>/', views.user_page, name='admin-porfile'),
    path('list/', views.profiles_page, name='admin-list-profiles')

]
