import time
from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View

from admission.forms import FileUploadForm, PortfolioForm
from admission.models import File, Participant
from itlAdmissionProject.settings import FILES_COUNT_LIMIT

from admission.models import Participant


class UploadView(View):
    def get(self, request):
        form = PortfolioForm(instance=Participant.objects.get(user=request.user))
        files_list = Participant.objects.get(user=request.user).portfolio.all()
        files_count = len(files_list)
        context = {
            'files': files_list, 'form': form,
            'files_count': files_count, 'files_count_limit': FILES_COUNT_LIMIT,
            'reg_status': Participant.objects.get(user=request.user).reg_status
        }
        return render(self.request, 'registration/../../templates/registration/register4.html', context)

    def post(self, request):
        # time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar
        # testing locally.
        form = FileUploadForm(self.request.POST, self.request.FILES)
        participant_reg_status = Participant.objects.get(user=request.user).reg_status
        files_count = len(Participant.objects.get(user=request.user).portfolio.all())
        if files_count < FILES_COUNT_LIMIT and form.is_valid():
            file = form.save()
            participant = Participant.objects.get(user=request.user)
            participant.portfolio.add(file)
            data = {
                'is_valid': True, 'name': file.file.name, 'url': file.file.url,
                'reg_status': participant_reg_status,  'is_limit_reached': False
            }
        else:
            if files_count == FILES_COUNT_LIMIT:
                er = 'Превышен лимит на количество загружаемых файлов!'
            else:
                er = 'br'.join(form.errors['file'])
            data = {
                'is_valid': False, 'error_message': er,
                'reg_status': participant_reg_status, 'is_limit_reached': True
            }
        return JsonResponse(data)


class PortfolioUploadView(View):
    def get(self, request):
        context = {'participant': Participant.objects.get(user=request.user)}
        return HttpResponseRedirect(redirect('admission:register4', context))

    def post(self, request):
        form = PortfolioForm(self.request.POST, instance=Participant.objects.get(user=request.user))
        base_url = reverse('admission:register4')
        url = f'{base_url}'
        if form.is_valid():
            # print(form.fields())
            form.save()
            return redirect('admission:register-done')
        else:
            query_string = urlencode({'error': True})
            url = f'{base_url}?{query_string}'

        return redirect(url)
