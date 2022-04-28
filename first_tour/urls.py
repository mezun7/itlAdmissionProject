import datetime

from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth import views as auth_views

from admin_profile.views import send_results
from itlAdmissionProject import settings
from itlAdmissionProject.settings import SERVER_EMAIL, REGISTER_END_DATE
from . import views
from first_tour.appeal.teacher_view import appeals_list, appeal_person
from admission import first_tour
from .final_results.main_raiting import main_table, journal_with_photos, edit_mark
from .views import get_registered, upload_sheets, exam_sheets, upload_results

app_name = 'first_tour'

urlpatterns = [
    path('main/', views.main, name='test-email'),
    path('appeal/', appeals_list, name='appeal-list'),
    path('appeal/<int:pk>/', appeal_person, name='appeal-person'),
    path('start-email/', send_results, name='send-results'),
    path('get-parties/', get_registered, name='get-registered'),
    path('final-table/', main_table, name='final-table'),
    path('final-table/<int:tour_ordering>/', main_table, name='final-table'),
    path('final-table/<int:tour_ordering>/<int:tour_id>/', main_table, name='final-table'),
    path('journal/', journal_with_photos, name='journal'),
    path('journal/<int:liter_id>/', journal_with_photos, name='journal'),
    path('edit_mark/<int:mark_id>', edit_mark, name='mark_edit'),
    # path('start-test/', send_results, name='send-test'),
    path('exam_sheets/', exam_sheets, name='exam_sheets'),
    path('upload_sheets/', upload_sheets, name='upload_sheets'),
    path('upload_results/', upload_results, name='upload_results'),
]
