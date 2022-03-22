import time
from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View

from admission.forms import FileUploadForm, PortfolioForm
from admission.models import File, Participant


class UploadView(View):
    def get(self, request):
        form = PortfolioForm(instance=Participant.objects.get(user=request.user))
        files_list = Participant.objects.get(user=request.user).portfolio.all()
        return render(self.request, 'registration/../../templates/registration/register4.html', {'files': files_list,
                                                                    'form': form})

    def post(self, request):
        # time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar
        # testing locally.
        form = FileUploadForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            file = form.save()
            participant = Participant.objects.get(user=request.user)
            participant.portfolio.add(file)
            data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        else:
            er = 'br'.join(form.errors['file'])

            data = {'is_valid': False, 'error_message': er}
        return JsonResponse(data)


class PortfolioUploadView(View):
    def get(self, request):
        return HttpResponseRedirect(redirect('admission:register4'))

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
