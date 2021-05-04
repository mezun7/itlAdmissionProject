from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth import views as auth_views

from itlAdmissionProject import settings
from itlAdmissionProject.settings import SERVER_EMAIL
from . import views
from .dashboard import main_dashboard
from .moderator import moderator
from .forms import AuthForm, PasswordResetForm, SetPasswordForm
from .register import main_register
from .register.upload import PortfolioUploadView, UploadView
from .personal_page import profile as profile
urlpatterns = [
    path('', views.proxy_func, name='home'),
    # path('test/', views.test_upload, name='test-upload'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=AuthForm),
         name='login'),
    path('reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', form_class=PasswordResetForm, from_email=SERVER_EMAIL),
         name='reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',
                                                                                form_class=SetPasswordForm),
         name='password_reset_confirm'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('email/', views.test_email, name='test-email'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('register/', main_register.register, name='register'),
    path('register_2/', main_register.register_2, name='register2'),
    path('register_3/', main_register.register_3, name='register3'),
    path('register_4/', login_required(UploadView.as_view()), name='register4'),
    path('confirm/<slug:activation_key>', main_register.confirm, name='confirm'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('portfolio_text/', login_required(PortfolioUploadView.as_view()), name='portfolio_text'),
    path('registration/done/', main_register.register_complete, name='register-done'),
    path('proxy/', views.proxy_func, name='proxy'),
    path('profile/', views.profile, name='main'),
    path('prf/', profile.profile_test_page, name='main-profile'),
    path('moderator/', moderator.moderator, name='moderator'),
    path('dashboard/', main_dashboard.dashboard_main, name='dashboard'),
    path('profile_moderator/<int:profile_id>/', moderator.moderate, name='profile-moderate')
    # path('testu/', UploadView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
