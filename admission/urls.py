from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .forms import AuthForm
from .register import main_register

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test_upload, name='test-upload'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=AuthForm),
         name='login'),
    path('email/', views.test_email, name='test-email'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', main_register.register, name='register'),
    path('register_2/', main_register.register_2, name='register2'),
    path('register_3/', main_register.register_3, name='register3')
]
