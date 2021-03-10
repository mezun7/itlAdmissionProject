import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from admission.models import Profile


def get_profile(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        grade = int(request.GET.get('grade', ''))
        profiles = Profile.objects.filter(grade__number=grade)
        result = []
        for profile in profiles:
            tmp_json = {'id': profile.id, 'label': profile.name, 'value': profile.name}
            result.append(tmp_json)
        data = json.dumps(result)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
