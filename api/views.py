import itertools
import json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from admission.models import Profile, Group, GENDER_CHOICES, Participant, STATUS_CHOICES, FirstTourDates

backgroundColors = ['#f56954', '#00a65a', '#00c0ef', '#3c8dbc', '#d2d6de', '#6c757d', ]

OptionsTemplate = {
    'maintainAspectRatio': False,
    'responsive': True,
    'elements': {
        'center': {
            'text': '3000',
            'color': '#36A2EB',
            'fontStyle': 'Helvetica',
            'sidePadding': 20
        }
    }
}


# TODO
# Delete
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
    registration_options = OptionsTemplate.copy()
    registration_options['elements']['center']['text'] = Participant.objects.filter(is_dublicate=False).count()

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
        res[str(grade.number) + " класс"] = [grade.participant_set.filter(is_dublicate=False).count() - tmp,
                                             backgroundColors[ind]]
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

    data = {
        'labels': labels,
        'datasets': [
            datasets,
        ]
    }

    final_result = {
        'options': registration_options,
        'data': data
    }
    data = json.dumps(final_result)
    if request.is_ajax():
        pass
    return HttpResponse(data, mimetype)


def get_all_gender(request):
    gender_options = OptionsTemplate.copy()

    datasets = {
        'data': [],
        'backgroundColor': []
    }
    result = {
        'labels': [x[1] for x in GENDER_CHOICES],
        'datasets': [datasets, ]
    }
    overall = 0
    for ind, gender in enumerate(GENDER_CHOICES):
        tmp = Participant.objects.filter(gender__iexact=gender[0], is_dublicate=False).count()
        overall += tmp
        datasets['data'].append(tmp)
        datasets['backgroundColor'].append(backgroundColors[ind])
    gender_options['elements']['center']['text'] = overall
    final_result = {
        'options': gender_options,
        'data': result
    }
    mimetype = 'application/json'

    return HttpResponse(json.dumps(final_result), mimetype)


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
    overall = 0
    for ind, status in enumerate(STATUS_CHOICES):
        sum2 = 0
        if status[0] == 'N':
            sum2 = Participant.objects.filter(out_of_competition=True, privilege_status__isnull=True,
                                              is_dublicate=False).count()
        tmp = Participant.objects.filter(
            privilege_status=status[0], is_dublicate=False).count() + sum2
        overall += tmp
        datasets['data'].append(tmp)
        datasets['backgroundColor'].append(colours[status[0]])

    mimetype = 'application/json'
    comp_options = OptionsTemplate.copy()
    comp_options['elements']['center']['text'] = overall
    final_result = {
        'options': comp_options,
        'data': result
    }

    return HttpResponse(json.dumps(final_result), mimetype)


def get_profiles(request):
    profile_options = OptionsTemplate.copy()
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
        'labels': [profile.name.split()[0] for profile in profiles],
        'datasets': [datasets, ]
    }
    overall = 0
    for ind, profile in enumerate(profiles):
        tmp = profile.participant_set.filter(is_dublicate=False).count()
        overall += tmp
        datasets['data'].append(tmp)
        datasets['backgroundColor'].append(backgroundColors[ind])
    profile_options['elements']['center']['text'] = overall
    profile_options['plugins'] = {
        'legend': {
            'position': 'right',
            'align': "middle"
        }
    }
    # plugins: {
    #     legend: {
    #         position: 'right',
    #     },
    final_result = {
        'options': profile_options,
        'data': result
    }
    mimetype = 'application/json'

    return HttpResponse(json.dumps(final_result), mimetype)


def get_date_distribution(request):
    dates = FirstTourDates.objects.all().order_by('date')
    datasets = {
        'data': [],
        'backgroundColor': []
    }
    result = {
        'labels': [fdate.date.strftime('%d/%m/%Y') for fdate in dates],
        'datasets': [datasets, ]
    }
    overall = 0
    for ind, fdate in enumerate(dates):
        tmp = fdate.participant_set.filter(is_dublicate=False).count()
        overall += tmp
        datasets['data'].append(tmp)
        datasets['backgroundColor'].append(backgroundColors[ind])
    mimetype = 'application/json'
    dates_options = OptionsTemplate.copy()
    dates_options['elements']['center']['text'] = overall
    final_result = {
        'options': dates_options,
        'data': result
    }
    return HttpResponse(json.dumps(final_result), mimetype)


def get_olymp_coming(request):
    colours = {
        'N': '#6c757d',
        'R': '#f56954',
        'A': '#00a65a',
    }
    NAMES = {
        'N': 'Не позвонили',
        'R': 'Не придет',
        'A': 'Придет',
    }
    datasets = {
        'data': [],
        'backgroundColor': []
    }
    result = {
        'labels': [NAMES[x[0]] for x in STATUS_CHOICES],
        'datasets': [datasets, ]
    }
    overall = 0
    for ind, status in enumerate(STATUS_CHOICES):
        tmp = Participant.objects.filter(
            olymp_coming_status=status[0], is_dublicate=False, privilege_status__iexact='A').count()
        overall += tmp
        datasets['data'].append(tmp)
        datasets['backgroundColor'].append(colours[status[0]])

    mimetype = 'application/json'
    comp_options = OptionsTemplate.copy()
    comp_options['elements']['center']['text'] = overall
    final_result = {
        'options': comp_options,
        'data': result
    }

    return HttpResponse(json.dumps(final_result), mimetype)


def get_first_tour_coming_register(request):
    datasets = {
        'data': [],
        'backgroundColor': []
    }
    first_tour_dates = FirstTourDates.objects.all().order_by('date')
    grades = Group.objects.all().order_by('number')
    product_dt_grades = itertools.product(first_tour_dates, grades)

    result = {
        'labels': ['Не пришли'],
        'datasets': [datasets, ]
    }
    overall = Participant.objects.filter(first_tour_come_date__isnull=True,
                                                       is_dublicate=False, first_name__isnull=False).count()
    ind = 0
    datasets['data'].append(overall)
    datasets['backgroundColor'].append('#6c757d')
    for ft_date, grade in product_dt_grades:
        tmp = Participant.objects.filter(
            first_tour_come_date__date=ft_date.date, grade=grade).count()
        overall += tmp

        result['labels'].append(str(ft_date.date) + " " + str(grade.number) + " Класс")
        datasets['data'].append(tmp)
        datasets['backgroundColor'].append(backgroundColors[ind])
        ind += 1
    # print(result['labels'], datasets['data'])

    mimetype = 'application/json'
    comp_options = OptionsTemplate.copy()
    comp_options['elements']['center']['text'] = overall
    final_result = {
        'options': comp_options,
        'data': result
    }

    return HttpResponse(json.dumps(final_result), mimetype)