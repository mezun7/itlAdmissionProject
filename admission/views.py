from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.
from admission.forms import FileUpload
from admission.models import File


def home(request):
    return HttpResponse("Hello!")


@login_required()
def test_upload(request):
    if request.method == 'POST':
        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('file'):
                file_instance = File(file=f)
                file_instance.save()
    else:
        form = FileUpload()
    return render(request, 'registration/base.html', {'form': form})


def test_email(request):
    send_mail('Test email', 'test message from django', 'shukhrat.azimuratov@litsey7.com', ['sa@litsey7.com', ],
              fail_silently=False)
    return HttpResponse("Success")
