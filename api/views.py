import json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from admission.models import Profile, Group, GENDER_CHOICES, Participant, STATUS_CHOICES, FirstTourDates

backgroundColors = ['#f56954', '#00a65a', '#00c0ef', '#3c8dbc', '#d2d6de', '#6c757d', ]


# data = {
#     'labels': [
#         'Chrome',
#         'IE',
#         'FireFox',
#         'Safari',
#         'Opera',
#         'Navigator'
#     ],
#     'datasets': [{
#         'data': [700, 500, 400, 600, 300, 100],
#         'backgroundColor': ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de'],
#     }]
# }


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


def get_all_registration(request):
    not_finished_label = 'Не завершили регистрацию'

    mimetype = 'application/json'
    grades = Group.objects.all().order_by('number')
    res = {

    }
    not_finished_registration = 0
    ind = 0
    for grade in grades:
        tmp = grade.participant_set.filter(reg_status__lt=99).count()
        not_finished_registration += tmp
        res[str(grade.number) + " класс"] = [grade.participant_set.all().count() - tmp, backgroundColors[ind]]
        ind += 1
    res[not_finished_label] = [not_finished_registration, backgroundColors[-1]]
    labels = []
    datasets = {
        'data': [],
        'backgroundColor': []
    }
    for k, v in res.items():
        labels.append(str(k))
        datasets['data'].append(v[0])
        datasets['backgroundColor'].append(v[1])

    print(datasets)
    data = {
        'labels': labels,
        'datasets': [
            datasets,
        ]
    }

    data = json.dumps(data)
    if request.is_ajax():
        pass
    return HttpResponse(data, mimetype)


def get_all_gender(request):
    datasets = {
        'data': [],
        'backgroundColor': []
    }
    result = {
        'labels': [x[1] for x in GENDER_CHOICES],
        'datasets': [datasets, ]
    }
    for ind, gender in enumerate(GENDER_CHOICES):
        datasets['data'].append(Participant.objects.filter(gender__iexact=gender[0]).count())
        datasets['backgroundColor'].append(backgroundColors[ind])
    print(datasets)
    mimetype = 'application/json'

    return HttpResponse(json.dumps(result), mimetype)


def get_out_of_competition(request):
    colours = {
        'N': '#6c757d',
        'R': '#f56954',
        'A': '#00a65a',
    }
    datasets = {
        'data': [],
        'backgroundColor': []
    }
    result = {
        'labels': [x[1] for x in STATUS_CHOICES],
        'datasets': [datasets, ]
    }

    for ind, status in enumerate(STATUS_CHOICES):
        sum2 = 0
        if status[0] == 'N':
            sum2 = Participant.objects.filter(out_of_competition=True, reg_status__isnull='').count()
        print(sum2)
        datasets['data'].append(Participant.objects.filter(
            privilege_status=status[0]).count() + sum2)

        datasets['backgroundColor'].append(colours[status[0]])
    mimetype = 'application/json'

    return HttpResponse(json.dumps(result), mimetype)


def get_profiles(request):
    profiles = Profile.objects.all().order_by('name')
    colours = {
        'N': '#6c757d',
        'R': '#f56954',
        'A': '#f56954',
    }
    datasets = {
        'data': [],
        'backgroundColor': []
    }
    result = {
        'labels': [profile.name for profile in profiles],
        'datasets': [datasets, ]
    }
    for ind, profile in enumerate(profiles):
        datasets['data'].append(profile.participant_set.all().count())
        datasets['backgroundColor'].append(backgroundColors[ind])
    mimetype = 'application/json'

    return HttpResponse(json.dumps(result), mimetype)


def get_date_distribution(request):
    dates = FirstTourDates.objects.all().order_by('date')
    datasets = {
        'data': [],
        'backgroundColor': []
    }
    result = {
        'labels': [fdate.date.strftime('%y-%m-%d') for fdate in dates],
        'datasets': [datasets, ]
    }

    for ind, fdate in enumerate(dates):
        datasets['data'].append(fdate.participant_set.all().count())
        datasets['backgroundColor'].append(backgroundColors[ind])
    mimetype = 'application/json'

    return HttpResponse(json.dumps(result), mimetype)
