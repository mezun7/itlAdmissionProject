from django.contrib import admin
from django.urls import path, include

import admission
from api import views

urlpatterns = [
    path('all/', views.get_all_registration, name='all-registrations'),
    path('gender/', views.get_all_gender, name='all-gender'),
    path('reg_status/', views.get_out_of_competition, name='competition'),
    path('profile/', views.get_profiles, name='profiles'),
    path('dates/', views.get_date_distribution, name='first-tour-distribution'),
    path('olymp_coming_status/', views.get_olymp_coming, name='olymp-coming-status-api')
]