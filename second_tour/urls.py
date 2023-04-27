from django.urls import path
from . import views

app_name = 'second_tour'

urlpatterns = [
    path('check_list/<int:pk>', views.check_list, name='check_list'),
    path('check_list/', views.check_list, name='check_list'),
    # path('check_list/litergrade_list/<int:pk>', views.get_litergrade_list, name='get_litergrade_list'),
    path('check_list/set_has_come', views.set_has_come, name='set_has_come'),
    path('check_list/set_participant_litergrade', views.set_participant_litergrade, name='set_participant_litergrade'),
    path('check_list/exclude_participant', views.exclude_participant, name='exclude_participant'),
    path('check_list/add_participant', views.add_participant, name='add_participant'),
    path('check_list/get_participants', views.get_participants, name='get-participants-2-tour')
]
